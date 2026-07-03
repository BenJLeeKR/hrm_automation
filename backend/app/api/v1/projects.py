import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.pjt_mst import create_project, get_project, list_projects, update_project
from app.schemas.pjt_mst import ProjectCreate, ProjectListResponse, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])

_TGT_TBL_NM = "PJT_MST"


@router.get(
    "", response_model=ProjectListResponse, dependencies=[Depends(require_permission("projects", "view"))]
)
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    pjt_stat_cd: str | None = Query(None, description="진행 상태 코드 (PLANNED/RUNNING/CLOSED/HOLD)"),
    db: Session = Depends(get_db),
) -> ProjectListResponse:
    """프로젝트 목록 조회 (로드맵 §8 다음 작업 1번)"""
    items, total = list_projects(db, skip=skip, limit=limit, pjt_stat_cd=pjt_stat_cd)
    return ProjectListResponse(total=total, skip=skip, limit=limit, items=items)


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def post_project(
    payload: ProjectCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("projects", "create")),
) -> ProjectOut:
    """프로젝트 등록"""
    try:
        project = create_project(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 프로젝트 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=project.PJT_ID,
        aft_val_json=ProjectOut.model_validate(project).model_dump(mode="json"),
    )
    return project


@router.patch("/{pjt_id}", response_model=ProjectOut)
def patch_project(
    pjt_id: uuid.UUID,
    payload: ProjectUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("projects", "update")),
) -> ProjectOut:
    """프로젝트 수정 — 전달된 필드만 갱신"""
    project = get_project(db, pjt_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="프로젝트를 찾을 수 없습니다.")

    before_snapshot = ProjectOut.model_validate(project).model_dump(mode="json")
    try:
        project = update_project(db, project, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 프로젝트 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=project.PJT_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=ProjectOut.model_validate(project).model_dump(mode="json"),
    )
    return project
