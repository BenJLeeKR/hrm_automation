import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.core.security import hash_password
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_role_mst import list_roles
from app.repositories.sys_user_mst import create_user, get_user, list_users, update_user
from app.schemas.sys_role_mst import RoleOut
from app.schemas.sys_user_mst import SysUserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

_TGT_TBL_NM = "SYS_USER_MST"


@router.get(
    "/roles", response_model=list[RoleOut], dependencies=[Depends(require_permission("settings_users", "view"))]
)
def get_roles(db: Session = Depends(get_db)) -> list[RoleOut]:
    """역할 목록 조회 — 사용자 관리 화면(SCR-015)의 "역할" 선택 드롭다운 용도(`GET /api/v1/users/roles`)."""
    return list_roles(db)


@router.get(
    "", response_model=list[SysUserOut], dependencies=[Depends(require_permission("settings_users", "view"))]
)
def get_users(
    role_id: uuid.UUID | None = Query(None, description="역할 ID로 필터링 (SYS_ROLE_MST.ROLE_ID)"),
    use_yn: bool | None = Query(None, description="계정 활성 여부 필터 — 생략 시 전체"),
    db: Session = Depends(get_db),
) -> list[SysUserOut]:
    """시스템 사용자 목록 조회 (로드맵 §8 "설정 화면 구현", SCR-015)"""
    return list_users(db, role_id=role_id, use_yn=use_yn)


@router.post("", response_model=SysUserOut, status_code=status.HTTP_201_CREATED)
def post_user(
    payload: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("settings_users", "create")),
) -> SysUserOut:
    """시스템 사용자 등록 (SCR-015 "계정 등록/수정 모달") — 비밀번호는 해시로만 저장한다."""
    data = payload.model_dump(exclude={"password"})
    data["ENCR_PWD"] = hash_password(payload.password)
    try:
        user = create_user(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 로그인 ID 또는 이메일입니다."
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=user.USER_ID,
        aft_val_json=SysUserOut.model_validate(user).model_dump(mode="json"),
    )
    return user


@router.patch("/{user_id}", response_model=SysUserOut)
def patch_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("settings_users", "update")),
) -> SysUserOut:
    """시스템 사용자 수정 (SCR-015 "계정 등록/수정 모달", §9-1) — 전달된 필드만 갱신.
    비밀번호 변경은 이번 범위에서 다루지 않음(별도 후속)."""
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    before_snapshot = SysUserOut.model_validate(user).model_dump(mode="json")
    try:
        user = update_user(db, user, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 이메일입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=user.USER_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=SysUserOut.model_validate(user).model_dump(mode="json"),
    )
    return user
