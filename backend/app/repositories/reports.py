import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.hr_skill_mst import HrSkillMst
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst
from app.repositories.dashboard import get_data_quality, get_dept_utilization, get_summary

_TOP_SKILL_LIMIT = 10  # SCR-013 "기술별 인력 분포 Top 10" 기준


def get_skill_distribution_top(db: Session, *, limit: int = _TOP_SKILL_LIMIT) -> list[dict]:
    """보유 인력이 많은 순으로 상위 N개 기술 분포 (SCR-013 "기술별 인력 분포 Top 10")."""
    stmt = (
        select(HrSkillMst.SKILL_ID, HrSkillMst.SKILL_NM, func.count(HrEmplSkillRel.EMPL_ID).label("employee_count"))
        .select_from(HrEmplSkillRel)
        .join(HrSkillMst, HrSkillMst.SKILL_ID == HrEmplSkillRel.SKILL_ID)
        .group_by(HrSkillMst.SKILL_ID, HrSkillMst.SKILL_NM)
        .order_by(func.count(HrEmplSkillRel.EMPL_ID).desc())
        .limit(limit)
    )
    return [
        {"SKILL_ID": row.SKILL_ID, "SKILL_NM": row.SKILL_NM, "employee_count": row.employee_count}
        for row in db.execute(stmt).all()
    ]


def build_report(db: Session, *, as_of: date) -> dict:
    """주간/월간 리포트 공통 데이터 (SCR-013 탭 1·2 — "주간 리포트와 동일 구조, 기간만
    월 단위" 설계에 따라 두 탭이 같은 집계를 공유한다). 대시보드 집계 함수를 그대로
    재사용하고, 리포트 전용 위젯인 "기술별 인력 분포"만 신규로 추가한다."""
    summary = get_summary(db, as_of=as_of)
    return {
        "as_of": as_of,
        "total_active_employees": summary["total_active_employees"],
        "available_count": summary["available_count"],
        "partial_count": summary["partial_count"],
        "full_count": summary["full_count"],
        "ending_count": summary["ending_this_month_count"],
        "job_missing_count": get_data_quality(db)["job_missing_count"],
        "dept_utilization": get_dept_utilization(db, as_of=as_of),
        "skill_distribution": get_skill_distribution_top(db),
    }


def _month_range(from_dt: date, to_dt: date) -> list[date]:
    """`from_dt`~`to_dt`(둘 다 매월 1일) 사이의 월 목록을 1일 기준으로 생성한다."""
    months = []
    cursor = date(from_dt.year, from_dt.month, 1)
    end = date(to_dt.year, to_dt.month, 1)
    while cursor <= end:
        months.append(cursor)
        next_month = cursor.month % 12 + 1
        next_year = cursor.year + (1 if cursor.month == 12 else 0)
        cursor = date(next_year, next_month, 1)
    return months


def _month_end(month_start: date) -> date:
    next_month = month_start.month % 12 + 1
    next_year = month_start.year + (1 if month_start.month == 12 else 0)
    return date(next_year, next_month, 1)


def build_utilization_matrix(
    db: Session, *, from_dt: date, to_dt: date, dept_id: uuid.UUID | None = None
) -> dict:
    """"월별 가동률 통계" 매트릭스 (SCR-013 탭 3, `ResourceManagement_v2.xlsx` "가동률_통계"
    시트 구조) — 인원×프로젝트별 월간 투입률, 소계, 연평균, 조직 평균 3단계를 계산한다.

    과거 스냅샷을 보관하지 않으므로(§9 "HR_AVAIL_SNAP_GEN 배치 미구현"과 동일 제약)
    `PJT_ASGN_HIS`의 시작/종료일을 기준으로 각 월의 실제 투입률을 즉시 재계산한다.
    """
    months = _month_range(from_dt, to_dt)
    period = [f"{m.year}-{m.month:02d}" for m in months]

    empl_stmt = (
        select(HrEmplMst.EMPL_ID, HrEmplMst.EMPL_NO, HrEmplMst.EMPL_NM, HrDeptMst.DEPT_NM)
        .join(HrDeptMst, HrDeptMst.DEPT_ID == HrEmplMst.DEPT_ID)
        .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")
        .order_by(HrEmplMst.EMPL_NO)
    )
    if dept_id is not None:
        empl_stmt = empl_stmt.where(HrEmplMst.DEPT_ID == dept_id)
    employee_rows = db.execute(empl_stmt).all()
    if not employee_rows:
        zero = [0.0] * len(months)
        return {"period": period, "employees": [], "org_avg": {"running_only": zero, "running_committed": zero, "all": zero}}

    empl_ids = [row.EMPL_ID for row in employee_rows]
    asgn_stmt = (
        select(
            PjtAsgnHis.EMPL_ID,
            PjtAsgnHis.PJT_ID,
            PjtMst.PJT_NM,
            PjtAsgnHis.ASGN_TYPE_CD,
            PjtAsgnHis.ALLOC_RT,
            PjtAsgnHis.ASGN_STRT_DT,
            PjtAsgnHis.ASGN_END_DT,
        )
        .join(PjtMst, PjtMst.PJT_ID == PjtAsgnHis.PJT_ID)
        .where(PjtAsgnHis.EMPL_ID.in_(empl_ids), PjtAsgnHis.ASGN_STAT_CD != "CANCELED")
    )
    assignments_by_empl: dict[uuid.UUID, list] = {empl_id: [] for empl_id in empl_ids}
    for row in db.execute(asgn_stmt):
        assignments_by_empl[row.EMPL_ID].append(row)

    employees_out = []
    # 조직 평균 계산용 — 월별로 (수행중만 / 수행중+투입준비중 / 전체) 각 사원의 해당 월
    # 투입률 합계를 모아뒀다가 평균낸다.
    running_sums: list[list[int]] = [[] for _ in months]
    running_committed_sums: list[list[int]] = [[] for _ in months]
    all_sums: list[list[int]] = [[] for _ in months]

    for empl in employee_rows:
        rows_by_key: dict[tuple, dict] = {}
        for a in assignments_by_empl[empl.EMPL_ID]:
            key = (a.PJT_ID, a.ASGN_TYPE_CD)
            row = rows_by_key.setdefault(
                key, {"pjt_nm": a.PJT_NM, "asgn_type_cd": a.ASGN_TYPE_CD, "monthly": [0] * len(months)}
            )
            for i, month_start in enumerate(months):
                month_end = _month_end(month_start)
                if a.ASGN_STRT_DT < month_end and (a.ASGN_END_DT is None or a.ASGN_END_DT >= month_start):
                    row["monthly"][i] += a.ALLOC_RT

        rows = list(rows_by_key.values())
        subtotal = [sum(r["monthly"][i] for r in rows) for i in range(len(months))]
        subtotal_running = [
            sum(r["monthly"][i] for r in rows if r["asgn_type_cd"] == "RUNNING") for i in range(len(months))
        ]
        subtotal_running_committed = [
            sum(r["monthly"][i] for r in rows if r["asgn_type_cd"] in ("RUNNING", "COMMITTED"))
            for i in range(len(months))
        ]
        for i in range(len(months)):
            running_sums[i].append(subtotal_running[i])
            running_committed_sums[i].append(subtotal_running_committed[i])
            all_sums[i].append(subtotal[i])

        annual_avg = round(sum(subtotal) / len(months), 1) if months else 0.0
        over_100_months = [period[i] for i in range(len(months)) if subtotal[i] > 100]

        employees_out.append(
            {
                "empl_no": empl.EMPL_NO,
                "empl_nm": empl.EMPL_NM,
                "dept_nm": empl.DEPT_NM,
                "rows": [
                    {**r, "avg": round(sum(r["monthly"]) / len(months), 1) if months else 0.0} for r in rows
                ],
                "subtotal": subtotal,
                "annual_avg": annual_avg,
                "over_100_months": over_100_months,
            }
        )

    def _avg(values: list[int]) -> float:
        return round(sum(values) / len(values), 1) if values else 0.0

    org_avg = {
        "running_only": [_avg(m) for m in running_sums],
        "running_committed": [_avg(m) for m in running_committed_sums],
        "all": [_avg(m) for m in all_sums],
    }

    return {"period": period, "employees": employees_out, "org_avg": org_avg}
