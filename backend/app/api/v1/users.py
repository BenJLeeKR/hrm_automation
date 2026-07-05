import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.core.security import hash_password
from app.db.session import get_db
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_role_mst import list_roles
from app.repositories.sys_user_mst import create_user, deactivate_user, get_user, list_users, update_user
from app.schemas.sys_role_mst import RoleOut
from app.schemas.sys_user_mst import SysUserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

_TGT_TBL_NM = "SYS_USER_MST"

# HR_MGR이 EMPL_ID 연결 계정에 배정할 수 있는 업무 역할 범위(설계서 §5.5 "직원 역할
# 배정", `PERMISSION_MATRIX.md` `settings_users` 섹션) — ADMIN/HR_MGR 승격은 제외.
_HR_MGR_ASSIGNABLE_ROLE_CODES = ("PM", "TEAM_LEAD", "EXEC", "EMPLOYEE", "VIEWER")


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
    비밀번호 변경은 이번 범위에서 다루지 않음(별도 후속).

    `HR_MGR`은 `settings_users.update` 권한이 있어도 `EMPL_ID` 연결 계정의 업무 역할
    (`ROLE_ID`)만 변경할 수 있다 — `ADMIN` 승격이나 `EMPL_ID`가 없는 시스템/외부 협력사
    계정 수정은 여전히 `ADMIN`만 가능하다. 이 값(role)·행(row) 단위 제약은 화면/버튼
    단위인 `PERM_JSON`으로 표현할 수 없어 여기서 직접 검증한다(§8 큐 1-4,
    `PERMISSION_MATRIX.md` §5-7 참조)."""
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    update_fields = payload.model_dump(exclude_unset=True)
    current_role = db.get(SysRoleMst, current_user.ROLE_ID)
    if current_role is not None and current_role.ROLE_CD == "HR_MGR":
        if user.EMPL_ID is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="사원과 연동되지 않은 계정은 수정할 수 없습니다."
            )
        if set(update_fields) - {"ROLE_ID"}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="업무 역할만 변경할 수 있습니다.")
        if "ROLE_ID" in update_fields:
            target_role = db.get(SysRoleMst, update_fields["ROLE_ID"])
            if target_role is None or target_role.ROLE_CD not in _HR_MGR_ASSIGNABLE_ROLE_CODES:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="지정할 수 없는 역할입니다.")

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


@router.delete("/{user_id}", response_model=SysUserOut)
def delete_user(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("settings_users", "delete")),
) -> SysUserOut:
    """계정 비활성화 (SCR-015 "계정 비활성화" 버튼, §9-1) — 로우를 삭제하지 않고
    `USE_YN=False`로 전환하는 소프트 삭제(사원 퇴직 처리와 동일한 원칙)."""
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    if not user.USE_YN:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 비활성화된 계정입니다.")

    before_snapshot = SysUserOut.model_validate(user).model_dump(mode="json")
    user = deactivate_user(db, user)

    record_audit(
        db,
        request,
        current_user,
        act_cd="DELETE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=user.USER_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=SysUserOut.model_validate(user).model_dump(mode="json"),
    )
    return user
