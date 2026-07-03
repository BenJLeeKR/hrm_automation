import calendar
import uuid
from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst
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


def get_data_quality(db: Session) -> dict:
    """데이터 품질 점검 요약 (프론트엔드 `/dashboard` 위젯 "데이터 품질 점검" 참조).

    `HR_DATA_QUALITY_CHK` 배치(Phase 7, 매주 금요일 18:00, 미구현)가 정기 점검을 전담할
    예정이나, 대시보드 위젯이 즉시 표시할 수 있도록 동일한 점검 3종을 실시간 조회로 제공한다.
    """
    skill_missing_count = (
        db.scalar(
            select(func.count())
            .select_from(HrEmplMst)
            .outerjoin(HrEmplSkillRel, HrEmplSkillRel.EMPL_ID == HrEmplMst.EMPL_ID)
            .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE", HrEmplSkillRel.EMPL_SKILL_ID.is_(None))
        )
        or 0
    )
    job_missing_count = (
        db.scalar(
            select(func.count())
            .select_from(HrEmplMst)
            .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE", HrEmplMst.JIKMU_ID.is_(None))
        )
        or 0
    )
    # 100% 초과 ALLOC_RT는 등록/수정 API에서 이미 저장 차단하지만(assignments.py), 기존 Excel
    # 이관 데이터 예외(AVAILABILITY_CALC_SPEC.md §5)를 대비해 사원별 합계를 다시 점검한다.
    over_allocation_stmt = (
        select(PjtAsgnHis.EMPL_ID)
        .where(PjtAsgnHis.ASGN_STAT_CD == "ACTIVE")
        .group_by(PjtAsgnHis.EMPL_ID)
        .having(func.sum(PjtAsgnHis.ALLOC_RT) > 100)
    )
    over_allocation_count = len(db.execute(over_allocation_stmt).all())

    return {
        "skill_missing_count": skill_missing_count,
        "job_missing_count": job_missing_count,
        "over_allocation_count": over_allocation_count,
    }


def get_ending_this_month(db: Session, *, as_of: date) -> list[dict]:
    """이번 달 투입 종료 예정 목록 (프론트엔드 `/dashboard` 위젯 참조)."""
    first_day = as_of.replace(day=1)
    last_day = date(as_of.year, as_of.month, calendar.monthrange(as_of.year, as_of.month)[1])

    stmt = (
        select(
            HrEmplMst.EMPL_NM,
            HrDeptMst.DEPT_NM,
            PjtMst.PJT_NM,
            PjtAsgnHis.ASGN_END_DT,
            PjtAsgnHis.ALLOC_RT,
        )
        .select_from(PjtAsgnHis)
        .join(HrEmplMst, HrEmplMst.EMPL_ID == PjtAsgnHis.EMPL_ID)
        .outerjoin(HrDeptMst, HrDeptMst.DEPT_ID == HrEmplMst.DEPT_ID)
        .join(PjtMst, PjtMst.PJT_ID == PjtAsgnHis.PJT_ID)
        .where(PjtAsgnHis.ASGN_STAT_CD == "ACTIVE", PjtAsgnHis.ASGN_END_DT.between(first_day, last_day))
        .order_by(PjtAsgnHis.ASGN_END_DT)
    )
    return [
        {
            "EMPL_NM": row.EMPL_NM,
            "DEPT_NM": row.DEPT_NM,
            "PJT_NM": row.PJT_NM,
            "ASGN_END_DT": row.ASGN_END_DT,
            "ALLOC_RT": row.ALLOC_RT,
        }
        for row in db.execute(stmt).all()
    ]


def get_recent_employees(db: Session, *, limit: int) -> list[dict]:
    """최근 입사자 목록 (프론트엔드 `/dashboard` 위젯 참조) — `HIRE_DT` 최신순."""
    stmt = (
        select(
            HrEmplMst.EMPL_NO,
            HrEmplMst.EMPL_NM,
            HrDeptMst.DEPT_NM,
            HrEmplMst.HIRE_DT,
            HrJikmuMst.JIKMU_NM,
        )
        .select_from(HrEmplMst)
        .outerjoin(HrDeptMst, HrDeptMst.DEPT_ID == HrEmplMst.DEPT_ID)
        .outerjoin(HrJikmuMst, HrJikmuMst.JIKMU_ID == HrEmplMst.JIKMU_ID)
        .where(HrEmplMst.EMPL_STAT_CD == "ACTIVE", HrEmplMst.HIRE_DT.is_not(None))
        .order_by(HrEmplMst.HIRE_DT.desc())
        .limit(limit)
    )
    return [
        {
            "EMPL_NO": row.EMPL_NO,
            "EMPL_NM": row.EMPL_NM,
            "DEPT_NM": row.DEPT_NM,
            "HIRE_DT": row.HIRE_DT,
            "JIKMU_NM": row.JIKMU_NM,
        }
        for row in db.execute(stmt).all()
    ]


def get_headcount_trend(db: Session, *, as_of: date, months: int) -> list[dict]:
    """월별 인력 추이 (프론트엔드 `/dashboard` "월별 인력 추이" 차트 참조).

    각 월말 기준 재직 인원(`total`)과 해당 월의 입사(`hires`)/퇴사(`exits`) 건수를 계산한다.
    `months`개월(당월 포함) 만큼 과거로 거슬러 올라간다.
    """
    result = []
    year, month = as_of.year, as_of.month
    for _ in range(months):
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])

        total = (
            db.scalar(
                select(func.count())
                .select_from(HrEmplMst)
                .where(
                    HrEmplMst.HIRE_DT.is_not(None),
                    HrEmplMst.HIRE_DT <= last_day,
                    or_(HrEmplMst.RETIR_DT.is_(None), HrEmplMst.RETIR_DT > last_day),
                )
            )
            or 0
        )
        hires = (
            db.scalar(
                select(func.count()).select_from(HrEmplMst).where(HrEmplMst.HIRE_DT.between(first_day, last_day))
            )
            or 0
        )
        exits = (
            db.scalar(
                select(func.count()).select_from(HrEmplMst).where(HrEmplMst.RETIR_DT.between(first_day, last_day))
            )
            or 0
        )

        result.append({"month": f"{year:04d}{month:02d}", "total": total, "hires": hires, "exits": exits})

        month -= 1
        if month == 0:
            month = 12
            year -= 1

    result.reverse()
    return result
