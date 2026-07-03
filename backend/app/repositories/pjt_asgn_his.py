import uuid
from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.pjt_asgn_his import PjtAsgnHis

# ALLOC_RT 합계 검증 시 집계 대상 상태 — 취소(CANCELED)/종료(DONE) 건은 더 이상 인력을
# 점유하지 않으므로 제외한다 (ERD §3.9 / 설계서 §5.5 "동일 사원 동일 기간 ALLOC_RT 합계
# 100% 초과 금지" 규칙의 MVP 해석, `HR_AVAIL_SNAP` 가동률 집계 조건(AVAILABILITY_CALC_SPEC.md)과
# 동일한 원칙을 재사용).
ACTIVE_ASGN_STAT_CODES = ("PLANNED", "ACTIVE")


def list_assignments(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    empl_id: uuid.UUID | None = None,
    pjt_id: uuid.UUID | None = None,
    asgn_stat_cd: str | None = None,
) -> tuple[list[PjtAsgnHis], int]:
    """투입 이력 목록 조회 — 사원/프로젝트/상태 필터, skip/limit 페이지네이션."""
    stmt = select(PjtAsgnHis)
    count_stmt = select(func.count()).select_from(PjtAsgnHis)

    if empl_id is not None:
        stmt = stmt.where(PjtAsgnHis.EMPL_ID == empl_id)
        count_stmt = count_stmt.where(PjtAsgnHis.EMPL_ID == empl_id)
    if pjt_id is not None:
        stmt = stmt.where(PjtAsgnHis.PJT_ID == pjt_id)
        count_stmt = count_stmt.where(PjtAsgnHis.PJT_ID == pjt_id)
    if asgn_stat_cd is not None:
        stmt = stmt.where(PjtAsgnHis.ASGN_STAT_CD == asgn_stat_cd)
        count_stmt = count_stmt.where(PjtAsgnHis.ASGN_STAT_CD == asgn_stat_cd)

    total = db.scalar(count_stmt) or 0
    items = list(db.scalars(stmt.order_by(PjtAsgnHis.ASGN_STRT_DT.desc()).offset(skip).limit(limit)))
    return items, total


def get_assignment(db: Session, asgn_id: uuid.UUID) -> PjtAsgnHis | None:
    return db.get(PjtAsgnHis, asgn_id)


def sum_overlapping_alloc_rt(
    db: Session,
    *,
    empl_id: uuid.UUID,
    strt_dt: date,
    end_dt: date | None,
    exclude_asgn_id: uuid.UUID | None = None,
) -> int:
    """동일 사원의 [strt_dt, end_dt] 기간과 겹치는 유효 투입 건의 ALLOC_RT 합계를 구한다.

    `end_dt=None`(종료일 미정)은 무기한 투입으로 간주해 겹침 조건에서 상한 없이 처리한다.
    """
    stmt = select(func.coalesce(func.sum(PjtAsgnHis.ALLOC_RT), 0)).where(
        PjtAsgnHis.EMPL_ID == empl_id,
        PjtAsgnHis.ASGN_STAT_CD.in_(ACTIVE_ASGN_STAT_CODES),
        or_(PjtAsgnHis.ASGN_END_DT.is_(None), PjtAsgnHis.ASGN_END_DT >= strt_dt),
    )
    if end_dt is not None:
        stmt = stmt.where(PjtAsgnHis.ASGN_STRT_DT <= end_dt)
    if exclude_asgn_id is not None:
        stmt = stmt.where(PjtAsgnHis.ASGN_ID != exclude_asgn_id)
    return db.scalar(stmt) or 0


def create_assignment(db: Session, data: dict) -> PjtAsgnHis:
    """투입 이력 등록. `EMPL_ID`/`PJT_ID` FK 위반은 호출부(API 라우터)에서
    `sqlalchemy.exc.IntegrityError`를 잡아 처리한다. ALLOC_RT 합계 100% 초과 검증도
    호출부에서 `sum_overlapping_alloc_rt`로 사전 확인한다."""
    assignment = PjtAsgnHis(**data)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def update_assignment(db: Session, assignment: PjtAsgnHis, data: dict) -> PjtAsgnHis:
    """전달된 필드만 갱신 (부분 업데이트)."""
    for field, value in data.items():
        setattr(assignment, field, value)
    db.commit()
    db.refresh(assignment)
    return assignment
