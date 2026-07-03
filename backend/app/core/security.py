from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class TokenError(Exception):
    """토큰이 없거나(만료 포함) 형식이 잘못된 경우 발생 — 호출부(API 라우터)에서 401로 변환한다."""


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


def _create_token(*, subject: str, token_type: str, expires_delta: timedelta, extra_claims: dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {"sub": subject, "type": token_type, "iat": now, "exp": now + expires_delta}
    payload.update(extra_claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(*, user_id: str, role_id: str) -> str:
    return _create_token(
        subject=user_id,
        token_type=ACCESS_TOKEN_TYPE,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={"role_id": role_id},
    )


def create_refresh_token(*, user_id: str) -> str:
    return _create_token(
        subject=user_id,
        token_type=REFRESH_TOKEN_TYPE,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        extra_claims={},
    )


def decode_token(token: str, *, expected_type: str) -> dict[str, Any]:
    """토큰을 검증·디코드한다. 서명/만료/타입이 올바르지 않으면 `TokenError`를 발생시킨다."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise TokenError("유효하지 않거나 만료된 토큰입니다.") from exc

    if payload.get("type") != expected_type:
        raise TokenError("토큰 종류가 올바르지 않습니다.")
    return payload
