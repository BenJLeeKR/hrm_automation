import calendar
import uuid
from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.pjt_asgn_his import PjtAsgnHis
from app.repositories.hr_avail_snap import active_alloc_rt_subquery

# 조직 평균 가동률 3단계 집계 대상 (`[DESIGN]HRM_Screen_Design.md` SCR-002 참조) —
# 화면 설계서는 데이터 소스를 HR_AVAIL_SNAP으로 명시하지만, 스냅샷 생성 배치
# HR_AVAIL_SNAP_GEN(Phase 7)이 아직 없어 테이블이 항상 비어 있다. 따라서 이 모듈은
# `active_alloc_rt_subquery`와 동일한 실시간 계산 로직(AVAILABILITY_CALC_SPEC.md)을
# 사원 단위로 집계해 대체한다 — Phase 7 배치 도입 후 스냅샷 테이블 기반 집계로 전환 가능.
_UTILIZATION_STAGE_TYPE_CODES = {
    "running": ("RUNNING",),
    "running_committed": ("RUNNING", "COMMITTED"),
    "all": ("RUNNING", "COMMITTED", "PROPOSED"),
}


def get_summary(db: Session, *, as_of: date) -> dict:
    """대시보드 KPI 카드 집계 (SCR-002)."""
    alloc_subq = active_alloc_rt_subquery(as_of)
    stmt = (
        select(func.coalesce(alloc_subq.c.tot_alloc_rt, 0).label("tot_alloc_rt"))
        .select_from(HrEmplMst)
        .outerjoin(alloc_subq, alloc_subq.c.EMPL_ID == HrEmplMst.EMPL_ID)
        .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")
    )
    alloc_rates = [row.tot_alloc_rt for row in db.execute(stmt).all()]
    total_active = len(alloc_rates)

    first_day = as_of.replace(day=1)
    last_day = date(as_of.year, as_of.month, calendar.monthrange(as_of.year, as_of.month)[1])
    ending_this_month = (
        db.scalar(
            select(func.count())
            .select_from(PjtAsgnHis)
            .where(PjtAsgnHis.ASGN_STAT_CD == "ACTIVE", PjtAsgnHis.ASGN_END_DT.between(first_day, last_day))
        )
        or 0
    )

    return {
        "total_active_employees": total_active,
        "available_count": sum(1 for rate in alloc_rates if rate == 0),
        "partial_count": sum(1 for rate in alloc_rates if 0 < rate < 100),
        "full_count": sum(1 for rate in alloc_rates if rate >= 100),
        "ending_this_month_count": ending_this_month,
        "avg_utilization_rate": (sum(alloc_rates) / total_active) if total_active else None,
    }


def get_dept_utilization(db: Session, *, as_of: date) -> list[dict]:
    """부서별 평균 가동률 (SCR-002) — 활성 사원이 1명 이상인 부서만 반환한다."""
    alloc_subq = active_alloc_rt_subquery(as_of)
    stmt = (
        select(
            HrDeptMst.DEPT_ID,
            HrDeptMst.DEPT_NM,
            func.coalesce(alloc_subq.c.tot_alloc_rt, 0).label("tot_alloc_rt"),
        )
        .select_from(HrDeptMst)
        .join(HrEmplMst, HrEmplMst.DEPT_ID == HrDeptMst.DEPT_ID)
        .outerjoin(alloc_subq, alloc_subq.c.EMPL_ID == HrEmplMst.EMPL_ID)
        .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")
        .order_by(HrDeptMst.DEPT_ORD)
    )

    by_dept: dict[uuid.UUID, dict] = {}
    for row in db.execute(stmt).all():
        entry = by_dept.setdefault(row.DEPT_ID, {"DEPT_ID": row.DEPT_ID, "DEPT_NM": row.DEPT_NM, "rates": []})
        entry["rates"].append(row.tot_alloc_rt)

    return [
        {
            "DEPT_ID": entry["DEPT_ID"],
            "DEPT_NM": entry["DEPT_NM"],
            "employee_count": len(entry["rates"]),
            "avg_utilization_rate": sum(entry["rates"]) / len(entry["rates"]),
        }
        for entry in by_dept.values()
    ]


def get_job_type_distribution(db: Session) -> list[dict]:
    """직무 유형별 인력 분포 (SCR-002) — 직무 유형 미등록 사원은 별도 그룹으로 집계한다."""
    stmt = (
        select(HrJikmuMst.JIKMU_ID, HrJikmuMst.JIKMU_NM, func.count(HrEmplMst.EMPL_ID).label("employee_count"))
        .select_from(HrEmplMst)
        .outerjoin(HrJikmuMst, HrJikmuMst.JIKMU_ID == HrEmplMst.JIKMU_ID)
        .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")
        .group_by(HrJikmuMst.JIKMU_ID, HrJikmuMst.JIKMU_NM)
        .order_by(HrJikmuMst.SORT_ORD)
    )
    return [
        {
            "JIKMU_ID": row.JIKMU_ID,
            "JIKMU_NM": row.JIKMU_NM or "직무 미등록",
            "employee_count": row.employee_count,
        }
        for row in db.execute(stmt).all()
    ]


def get_utilization_by_type(db: Session, *, year: int, month: int) -> dict:
    """3단계 조직 평균 가동률 (SCR-002) — 해당 월과 기간이 겹치는 유효 투입만 집계한다.

    화면 설계서는 일 단위가 아닌 월 단위 기준(`기준월: yyyy-MM`)이라, 다른 API의
    "기준일" 시점 계산과 달리 해당 월 전체와 겹치는 투입(`ASGN_STRT_DT<=월말`,
    `ASGN_END_DT IS NULL OR ASGN_END_DT>=월초`)을 대상으로 한다.
    """
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    total_active = (
        db.scalar(select(func.count()).select_from(HrEmplMst).where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")) or 0
    )

    def _alloc_rt_sum(type_codes: tuple[str, ...]) -> int:
        stmt = select(func.coalesce(func.sum(PjtAsgnHis.ALLOC_RT), 0)).where(
            PjtAsgnHis.ASGN_STAT_CD == "ACTIVE",
            PjtAsgnHis.ASGN_STRT_DT <= last_day,
            or_(PjtAsgnHis.ASGN_END_DT.is_(None), PjtAsgnHis.ASGN_END_DT >= first_day),
            PjtAsgnHis.ASGN_TYPE_CD.in_(type_codes),
        )
        return db.scalar(stmt) or 0

    def _rate(tot_alloc_rt: int) -> float:
        return round(tot_alloc_rt / total_active, 1) if total_active else 0.0

    return {
        "month": f"{year:04d}{month:02d}",
        "running_rate": _rate(_alloc_rt_sum(_UTILIZATION_STAGE_TYPE_CODES["running"])),
        "running_committed_rate": _rate(_alloc_rt_sum(_UTILIZATION_STAGE_TYPE_CODES["running_committed"])),
        "all_rate": _rate(_alloc_rt_sum(_UTILIZATION_STAGE_TYPE_CODES["all"])),
    }
