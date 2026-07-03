import uuid
from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Subquery

from app.models.pjt_asgn_his import PjtAsgnHis

# 가동률 계산 대상 투입 조건 (backend/docs/AVAILABILITY_CALC_SPEC.md §2) —
# ASGN_STAT_CD='ACTIVE', 기준일이 투입 기간 내, ASGN_TYPE_CD가 RUNNING/COMMITTED인 건만
# 집계한다. PROPOSED(제안중)는 기본 산정에서 제외(스펙 §3) — 참고용 "전체(+제안중)"
# 지표는 Phase 5/7 화면·리포트 구현 시 별도로 다룬다.
_CALC_TARGET_ASGN_TYPE_CODES = ("RUNNING", "COMMITTED")


@dataclass
class AvailabilityCalcResult:
    """가동률 계산 결과 — `HR_AVAIL_SNAP` 컬럼과 동일한 필드를 갖되, 이 계산은 매일 01:00
    배치 `HR_AVAIL_SNAP_GEN`(Phase 7, 미구현)이 스냅샷 행을 생성하는 것과 달리 즉시 계산만
    수행하고 `HR_AVAIL_SNAP` 테이블에 저장하지 않는다 — 로드맵 §8/§9 스펙 문서 참조."""

    EMPL_ID: uuid.UUID
    SNAP_DT: date
    TOT_ALLOC_RT: int
    AVAIL_RT: int
    AVAIL_STRT_DT: date | None
    AVAIL_STAT_CD: str
    DATA_QUALITY_WARNING: bool


def compute_availability(db: Session, *, empl_id: uuid.UUID, snap_dt: date) -> AvailabilityCalcResult:
    """`AVAILABILITY_CALC_SPEC.md` §2/§4 로직 그대로 구현한 단건 계산.

    기준일(`snap_dt`) 현재 유효한 투입(§2 조건)의 `ALLOC_RT` 합계로 `AVAIL_STAT_CD`/
    `AVAIL_STRT_DT`를 산정한다. 100% 이상이면서 집계 대상 중 `ASGN_END_DT`가 NULL인
    행이 있으면 `AVAIL_STRT_DT=None`으로 두고 `DATA_QUALITY_WARNING=True`로 표시한다.
    """
    stmt = select(PjtAsgnHis.ALLOC_RT, PjtAsgnHis.ASGN_END_DT).where(
        PjtAsgnHis.EMPL_ID == empl_id,
        PjtAsgnHis.ASGN_STAT_CD == "ACTIVE",
        PjtAsgnHis.ASGN_STRT_DT <= snap_dt,
        or_(PjtAsgnHis.ASGN_END_DT.is_(None), PjtAsgnHis.ASGN_END_DT >= snap_dt),
        PjtAsgnHis.ASGN_TYPE_CD.in_(_CALC_TARGET_ASGN_TYPE_CODES),
    )
    rows = db.execute(stmt).all()

    tot_alloc_rt = sum(row.ALLOC_RT for row in rows)
    avail_rt = max(0, 100 - tot_alloc_rt)

    if tot_alloc_rt == 0:
        avail_stat_cd, avail_strt_dt, data_quality_warning = "AVAILABLE", snap_dt, False
    elif tot_alloc_rt < 100:
        avail_stat_cd, avail_strt_dt, data_quality_warning = "PARTIAL", snap_dt, False
    else:
        end_dates = [row.ASGN_END_DT for row in rows]
        if any(end_dt is None for end_dt in end_dates):
            avail_stat_cd, avail_strt_dt, data_quality_warning = "FULL", None, True
        else:
            avail_stat_cd = "FULL"
            avail_strt_dt = max(end_dates) + timedelta(days=1)
            data_quality_warning = False

    return AvailabilityCalcResult(
        EMPL_ID=empl_id,
        SNAP_DT=snap_dt,
        TOT_ALLOC_RT=tot_alloc_rt,
        AVAIL_RT=avail_rt,
        AVAIL_STRT_DT=avail_strt_dt,
        AVAIL_STAT_CD=avail_stat_cd,
        DATA_QUALITY_WARNING=data_quality_warning,
    )


def active_alloc_rt_subquery(as_of: date) -> Subquery:
    """기준일 현재 유효한 투입(§2 조건과 동일 — `RUNNING`/`COMMITTED`만)의 사원별
    `ALLOC_RT` 합계 서브쿼리. `compute_availability`의 단건 계산과 동일한 산정 조건을
    대시보드 집계(`app/repositories/dashboard.py`)에서도 그대로 재사용하기 위해 추출했다."""
    return (
        select(
            PjtAsgnHis.EMPL_ID.label("EMPL_ID"),
            func.coalesce(func.sum(PjtAsgnHis.ALLOC_RT), 0).label("tot_alloc_rt"),
        )
        .where(
            PjtAsgnHis.ASGN_STAT_CD == "ACTIVE",
            PjtAsgnHis.ASGN_STRT_DT <= as_of,
            or_(PjtAsgnHis.ASGN_END_DT.is_(None), PjtAsgnHis.ASGN_END_DT >= as_of),
            PjtAsgnHis.ASGN_TYPE_CD.in_(_CALC_TARGET_ASGN_TYPE_CODES),
        )
        .group_by(PjtAsgnHis.EMPL_ID)
        .subquery()
    )
