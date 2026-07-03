import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.core.pagination import PaginationParams
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.pjt_asgn_his import (
    create_assignment,
    get_assignment,
    list_assignments,
    sum_overlapping_alloc_rt,
    update_assignment,
)
from app.schemas.pjt_asgn_his import AssignmentCreate, AssignmentListResponse, AssignmentOut, AssignmentUpdate

router = APIRouter(prefix="/assignments", tags=["assignments"])

_FK_ERROR_DETAIL = "사원/프로젝트 ID가 유효하지 않습니다."
_TGT_TBL_NM = "PJT_ASGN_HIS"


@router.get(
    "", response_model=AssignmentListResponse, dependencies=[Depends(require_permission("assignments", "view"))]
)
def get_assignments(
    pagination: PaginationParams = Depends(),
    empl_id: uuid.UUID | None = Query(None, description="사원 ID로 필터링 (HR_EMPL_MST.EMPL_ID)"),
    pjt_id: uuid.UUID | None = Query(None, description="프로젝트 ID로 필터링 (PJT_MST.PJT_ID)"),
    asgn_stat_cd: str | None = Query(None, description="투입 상태 코드 (PLANNED/ACTIVE/DONE/CANCELED)"),
    db: Session = Depends(get_db),
) -> AssignmentListResponse:
    """투입 이력 목록 조회 (로드맵 §8 다음 작업 1번)"""
    items, total = list_assignments(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        empl_id=empl_id,
        pjt_id=pjt_id,
        asgn_stat_cd=asgn_stat_cd,
    )
    return AssignmentListResponse(total=total, skip=pagination.skip, limit=pagination.limit, items=items)


@router.post("", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def post_assignment(
    payload: AssignmentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("assignments", "create")),
) -> AssignmentOut:
    """투입 이력 등록 — 동일 사원·겹치는 기간의 유효(`PLANNED`/`ACTIVE`) ALLOC_RT 합계가
    100%를 초과하면 409로 거부한다 (ERD §3.9 / 설계서 §5.5 정합성 규칙)."""
    if payload.ASGN_STAT_CD in ("PLANNED", "ACTIVE"):
        overlapping_total = sum_overlapping_alloc_rt(
            db, empl_id=payload.EMPL_ID, strt_dt=payload.ASGN_STRT_DT, end_dt=payload.ASGN_END_DT
        )
        if overlapping_total + payload.ALLOC_RT > 100:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"해당 기간 투입률 합계가 100%를 초과합니다 (기존 {overlapping_total}% + 신규 {payload.ALLOC_RT}%).",
            )

    try:
        assignment = create_assignment(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=_FK_ERROR_DETAIL) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=assignment.ASGN_ID,
        aft_val_json=AssignmentOut.model_validate(assignment).model_dump(mode="json"),
    )
    return assignment


@router.patch("/{asgn_id}", response_model=AssignmentOut)
def patch_assignment(
    asgn_id: uuid.UUID,
    payload: AssignmentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("assignments", "update")),
) -> AssignmentOut:
    """투입 이력 수정 — 전달된 필드만 갱신. ALLOC_RT/기간/상태 변경 시 100% 초과 여부를 재검증한다."""
    assignment = get_assignment(db, asgn_id)
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="투입 이력을 찾을 수 없습니다.")

    before_snapshot = AssignmentOut.model_validate(assignment).model_dump(mode="json")
    update_data = payload.model_dump(exclude_unset=True)
    new_stat = update_data.get("ASGN_STAT_CD", assignment.ASGN_STAT_CD)
    if new_stat in ("PLANNED", "ACTIVE"):
        new_alloc_rt = update_data.get("ALLOC_RT", assignment.ALLOC_RT)
        new_strt_dt = update_data.get("ASGN_STRT_DT", assignment.ASGN_STRT_DT)
        new_end_dt = update_data.get("ASGN_END_DT", assignment.ASGN_END_DT)
        overlapping_total = sum_overlapping_alloc_rt(
            db, empl_id=assignment.EMPL_ID, strt_dt=new_strt_dt, end_dt=new_end_dt, exclude_asgn_id=asgn_id
        )
        if overlapping_total + new_alloc_rt > 100:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"해당 기간 투입률 합계가 100%를 초과합니다 (기존 {overlapping_total}% + 신규 {new_alloc_rt}%).",
            )

    try:
        assignment = update_assignment(db, assignment, update_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=_FK_ERROR_DETAIL) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=assignment.ASGN_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=AssignmentOut.model_validate(assignment).model_dump(mode="json"),
    )
    return assignment
