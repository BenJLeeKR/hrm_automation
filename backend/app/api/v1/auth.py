import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.audit import record_audit
from app.core.security import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.token_blacklist import blacklist_token
from app.db.session import get_db
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_user_mst import get_user, get_user_by_login_id, update_last_login, update_user
from app.schemas.auth import (
    AccessTokenResponse,
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    MeOut,
    MeUpdate,
    RefreshRequest,
    TokenResponse,
)
from app.schemas.sys_user_mst import SysUserOut

_bearer_scheme = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["auth"])

_INVALID_CREDENTIALS_DETAIL = "아이디 또는 비밀번호가 올바르지 않습니다."


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    """로그인 — `SYS_USER_MST.USER_LGID`/비밀번호 검증 후 액세스/리프레시 토큰 발급"""
    user = get_user_by_login_id(db, payload.USER_LGID)
    # 계정 존재 여부를 노출하지 않도록 미존재/비밀번호 불일치/비활성/비밀번호 미설정을 모두 동일한 401로 처리한다.
    # 실패한 로그인 시도는 SYS_AUDIT_LOG.USER_ID가 NOT NULL FK라 행위자를 특정할 수 없어 기록하지 않는다.
    if user is None or not user.USE_YN or not user.ENCR_PWD or not verify_password(payload.password, user.ENCR_PWD):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_INVALID_CREDENTIALS_DETAIL)

    update_last_login(db, user)
    record_audit(db, request, user, act_cd="LOGIN", tgt_tbl_nm="SYS_USER_MST", tgt_id=user.USER_ID)
    return TokenResponse(
        access_token=create_access_token(user_id=str(user.USER_ID), role_id=str(user.ROLE_ID)),
        refresh_token=create_refresh_token(user_id=str(user.USER_ID)),
    )


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> AccessTokenResponse:
    """토큰 갱신 — 유효한 리프레시 토큰으로 새 액세스 토큰만 발급한다(리프레시 토큰은 재발급하지 않음)."""
    try:
        token_payload = decode_token(payload.refresh_token, expected_type=REFRESH_TOKEN_TYPE)
        user_id = uuid.UUID(token_payload["sub"])
    except (TokenError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않거나 만료된 토큰입니다.") from exc

    user = get_user(db, user_id)
    if user is None or not user.USE_YN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="사용자를 찾을 수 없거나 비활성 상태입니다.")

    return AccessTokenResponse(access_token=create_access_token(user_id=str(user.USER_ID), role_id=str(user.ROLE_ID)))


def _blacklist_if_valid(token: str, *, expected_type: str) -> None:
    """만료·서명 오류 등으로 이미 무효한 토큰은 블랙리스트에 추가할 필요가 없어 조용히
    건너뛴다 — 로그아웃 자체는 항상 성공해야 하므로 여기서 예외를 밖으로 던지지 않는다."""
    try:
        payload = decode_token(token, expected_type=expected_type)
    except TokenError:
        return
    blacklist_token(payload["jti"], datetime.fromtimestamp(payload["exp"], tz=timezone.utc))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    payload: LogoutRequest | None = None,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> None:
    """로그아웃 (§9-1 "로그아웃 시 서버 측 즉시 토큰 무효화 미구현" 해소) — 요청에 담긴
    액세스 토큰을 즉시 Redis 블랙리스트에 등록해 만료 전이라도 재사용을 막는다
    (`app/core/token_blacklist.py`). `refresh_token`을 함께 전달하면 그것도 함께
    무효화해, 액세스 토큰 재발급(`POST /auth/refresh`)까지 막을 수 있다."""
    if credentials:
        _blacklist_if_valid(credentials.credentials, expected_type=ACCESS_TOKEN_TYPE)
    if payload and payload.refresh_token:
        _blacklist_if_valid(payload.refresh_token, expected_type=REFRESH_TOKEN_TYPE)
    return None


def _build_me_out(db: Session, user: SysUserMst) -> MeOut:
    role = db.get(SysRoleMst, user.ROLE_ID)
    return MeOut(
        USER_ID=user.USER_ID,
        USER_LGID=user.USER_LGID,
        EMAIL_ADDR=user.EMAIL_ADDR,
        ROLE_CD=role.ROLE_CD if role else "",
        ROLE_NM=role.ROLE_NM if role else "",
        PERM_JSON=role.PERM_JSON if role else None,
    )


@router.get("/me", response_model=MeOut)
def get_me(current_user: SysUserMst = Depends(get_current_user), db: Session = Depends(get_db)) -> MeOut:
    """현재 로그인 사용자 정보 및 역할 권한(`PERM_JSON`) 조회 — 프론트엔드가 화면별
    접근 권한에 따라 사이드바 메뉴를 필터링하는 데 사용한다."""
    return _build_me_out(db, current_user)


@router.patch("/me", response_model=MeOut)
def update_me(
    payload: MeUpdate,
    request: Request,
    current_user: SysUserMst = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MeOut:
    """본인 정보 수정 (§9-1 "내 프로필" 화면) — 관리자용 `PATCH /users/{user_id}`와 달리
    별도 권한 검사 없이 로그인 사용자 본인만 대상으로 한다(URL에 대상 ID가 없어 다른
    계정을 수정할 방법이 없다)."""
    before_snapshot = SysUserOut.model_validate(current_user).model_dump(mode="json")
    try:
        current_user = update_user(db, current_user, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 이메일입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm="SYS_USER_MST",
        tgt_id=current_user.USER_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=SysUserOut.model_validate(current_user).model_dump(mode="json"),
    )
    return _build_me_out(db, current_user)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    payload: ChangePasswordRequest,
    request: Request,
    current_user: SysUserMst = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """비밀번호 변경 (설계서 §6 API 목록에 이미 명시, §9-1 "설정" 메뉴를 "비밀번호 변경"으로
    교체) — 현재 비밀번호 확인 후 본인 비밀번호만 교체한다. 비밀번호 값은 감사 로그에도
    남기지 않는다(`SysUserOut`이 `ENCR_PWD`를 응답에서 제외하는 것과 동일한 원칙)."""
    if not current_user.ENCR_PWD or not verify_password(payload.current_password, current_user.ENCR_PWD):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="현재 비밀번호가 올바르지 않습니다.")

    update_user(db, current_user, {"ENCR_PWD": hash_password(payload.new_password)})
    record_audit(db, request, current_user, act_cd="UPDATE", tgt_tbl_nm="SYS_USER_MST", tgt_id=current_user.USER_ID)
    return None
