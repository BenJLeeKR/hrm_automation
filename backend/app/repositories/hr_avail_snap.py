import uuid
from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Subquery

from app.models.hr_avail_snap import HrAvailSnap
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_skill_rel import HrEmplSkillRel
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


def _classify(
    *, empl_id: uuid.UUID, snap_dt: date, alloc_rows: list
) -> AvailabilityCalcResult:
    """`AVAILABILITY_CALC_SPEC.md` §2/§4 산정 로직 — 투입 건 목록(ALLOC_RT/ASGN_END_DT)에서
    `AVAIL_STAT_CD`/`AVAIL_STRT_DT`를 계산한다. 단건 계산(`compute_availability`)과
    전체 목록 계산(`list_availability`)이 동일한 로직을 공유하기 위해 추출했다."""
    tot_alloc_rt = sum(row.ALLOC_RT for row in alloc_rows)
    avail_rt = max(0, 100 - tot_alloc_rt)

    if tot_alloc_rt == 0:
        avail_stat_cd, avail_strt_dt, data_quality_warning = "AVAILABLE", snap_dt, False
    elif tot_alloc_rt < 100:
        avail_stat_cd, avail_strt_dt, data_quality_warning = "PARTIAL", snap_dt, False
    else:
        end_dates = [row.ASGN_END_DT for row in alloc_rows]
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
    return _classify(empl_id=empl_id, snap_dt=snap_dt, alloc_rows=rows)


def list_availability(
    db: Session,
    *,
    snap_dt: date,
    jikmu_id: uuid.UUID | None = None,
    dept_id: uuid.UUID | None = None,
    skill_id: uuid.UUID | None = None,
    min_prfcy_levl: int | None = None,
) -> list[AvailabilityCalcResult]:
    """재직 사원 전체 대상 가동률 일괄 계산 (SCR-010 "가동 가능 인력" 화면용).

    사원별로 `compute_availability`를 반복 호출하면 N+1 쿼리가 발생하므로, 대상 사원의
    투입 이력을 한 번에 조회한 뒤 파이썬에서 사원별로 묶어 동일한 산정 로직(`_classify`)을
    적용한다. `HR_AVAIL_SNAP_GEN` 배치(Phase 7, 미구현)와 마찬가지로 결과를 테이블에
    저장하지 않는 즉시 계산이다.

    `skill_id`/`min_prfcy_levl`(로드맵 §8 "직무 유형·기술·숙련도 복합 필터 검색 API 구현")는
    `HR_EMPL_SKILL_REL`에 해당 기술을 보유(숙련도 조건 포함)한 사원만 포함시키는 필터다.
    `min_prfcy_levl`만 단독으로 주어지면(기준이 될 기술이 없어) 무시한다.
    """
    employee_stmt = select(HrEmplMst.EMPL_ID).where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")
    if jikmu_id is not None:
        employee_stmt = employee_stmt.where(HrEmplMst.JIKMU_ID == jikmu_id)
    if dept_id is not None:
        employee_stmt = employee_stmt.where(HrEmplMst.DEPT_ID == dept_id)
    if skill_id is not None:
        skill_stmt = select(HrEmplSkillRel.EMPL_ID).where(HrEmplSkillRel.SKILL_ID == skill_id)
        if min_prfcy_levl is not None:
            skill_stmt = skill_stmt.where(HrEmplSkillRel.PRFCY_LEVL >= min_prfcy_levl)
        employee_stmt = employee_stmt.where(HrEmplMst.EMPL_ID.in_(skill_stmt))
    employee_ids = list(db.scalars(employee_stmt))
    if not employee_ids:
        return []

    assignment_stmt = select(PjtAsgnHis.EMPL_ID, PjtAsgnHis.ALLOC_RT, PjtAsgnHis.ASGN_END_DT).where(
        PjtAsgnHis.EMPL_ID.in_(employee_ids),
        PjtAsgnHis.ASGN_STAT_CD == "ACTIVE",
        PjtAsgnHis.ASGN_STRT_DT <= snap_dt,
        or_(PjtAsgnHis.ASGN_END_DT.is_(None), PjtAsgnHis.ASGN_END_DT >= snap_dt),
        PjtAsgnHis.ASGN_TYPE_CD.in_(_CALC_TARGET_ASGN_TYPE_CODES),
    )
    rows_by_empl: dict[uuid.UUID, list] = {empl_id: [] for empl_id in employee_ids}
    for row in db.execute(assignment_stmt):
        rows_by_empl[row.EMPL_ID].append(row)

    return [
        _classify(empl_id=empl_id, snap_dt=snap_dt, alloc_rows=rows_by_empl[empl_id])
        for empl_id in employee_ids
    ]


def generate_avail_snap(db: Session, *, snap_dt: date) -> int:
    """`HR_AVAIL_SNAP_GEN` 배치(로드맵 §8, 매일 01:00 실행) 본체 — `list_availability`와
    동일한 산정 로직으로 재직 사원 전체의 가동률을 계산해 `HR_AVAIL_SNAP`에 스냅샷
    행으로 저장한다. 재직 사원 전체 대상(부서/직무 필터 없음)이라는 점만 화면용
    `list_availability` 호출과 다르다.

    같은 `snap_dt`로 재실행해도 안전하도록(배치 수동 재실행 대비) 해당 날짜의 기존
    스냅샷을 먼저 삭제한 뒤 새로 삽입한다 — 커밋은 호출부(배치 실행기)에서 담당한다.
    """
    db.execute(delete(HrAvailSnap).where(HrAvailSnap.SNAP_DT == snap_dt))

    results = list_availability(db, snap_dt=snap_dt)
    for result in results:
        db.add(
            HrAvailSnap(
                EMPL_ID=result.EMPL_ID,
                SNAP_DT=result.SNAP_DT,
                TOT_ALLOC_RT=result.TOT_ALLOC_RT,
                AVAIL_RT=result.AVAIL_RT,
                AVAIL_STRT_DT=result.AVAIL_STRT_DT,
                AVAIL_STAT_CD=result.AVAIL_STAT_CD,
            )
        )
    return len(results)


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
