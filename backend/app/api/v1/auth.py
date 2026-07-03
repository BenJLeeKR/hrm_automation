import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.audit import record_audit
from app.core.security import (
    REFRESH_TOKEN_TYPE,
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.db.session import get_db
from app.repositories.sys_user_mst import get_user, get_user_by_login_id, update_last_login
from app.schemas.auth import AccessTokenResponse, LoginRequest, RefreshRequest, TokenResponse

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


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout() -> None:
    """로그아웃 — 현재 JWT는 서버 상태를 갖지 않는 stateless 토큰이라 서버 측에서 즉시
    무효화할 저장소(예: Redis 블랙리스트)가 아직 없다. RBAC 권한 미들웨어(로드맵 §8 다음 작업)
    구현 시 토큰 검증 경로가 추가되면 함께 도입 예정 — 그 전까지는 클라이언트가 저장된
    토큰을 폐기하는 것으로 로그아웃을 처리한다."""
    return None
