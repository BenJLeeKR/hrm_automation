import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.token_blacklist import is_blacklisted

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

# 임시 비밀번호 자동 생성용 문자 집합 — `app/schemas/sys_user_mst.py`의 비밀번호 정책
# (8자 이상, 영문·숫자·특수문자 포함)을 항상 만족하도록 3종을 각 1자 이상 보장한다.
_TEMP_PASSWORD_LENGTH = 12
_TEMP_PASSWORD_SPECIAL_CHARS = "!@#$%^&*"


class TokenError(Exception):
    """토큰이 없거나(만료 포함) 형식이 잘못된 경우 발생 — 호출부(API 라우터)에서 401로 변환한다."""


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def generate_temp_password() -> str:
    """사원 계정 자동 생성(설계서 §5.5 "사원 계정 자동 생성") 시 서버가 발급하는 임시
    비밀번호를 생성한다 — 영문·숫자·특수문자를 각 1자 이상 포함해 `UserCreate`의
    비밀번호 정책을 항상 만족시킨다."""
    required = [secrets.choice(string.ascii_letters), secrets.choice(string.digits), secrets.choice(_TEMP_PASSWORD_SPECIAL_CHARS)]
    pool = string.ascii_letters + string.digits + _TEMP_PASSWORD_SPECIAL_CHARS
    remaining = [secrets.choice(pool) for _ in range(_TEMP_PASSWORD_LENGTH - len(required))]
    chars = required + remaining
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def resolve_initial_password() -> str:
    """사원 계정 자동 생성 시 사용할 초기 비밀번호를 결정한다 — 운영팀 요청(2026-07-06)에
    따라 `.env`의 `EMPLOYEE_INITIAL_PASSWORD`가 설정되어 있으면 그 값을 우선 사용하고,
    미설정 시에는 `generate_temp_password()`로 무작위 생성한다(하위 호환 기본값). 사원
    등록(`app/api/v1/employees.py`)과 계정 없는 기존 사원 백필
    (`app/db/backfill_employee_accounts.py`) 양쪽에서 재사용한다."""
    return settings.EMPLOYEE_INITIAL_PASSWORD or generate_temp_password()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


def _create_token(*, subject: str, token_type: str, expires_delta: timedelta, extra_claims: dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)
    # jti(JWT ID) — 로그아웃 시 이 토큰만 개별적으로 블랙리스트 등록하기 위한 고유 식별자
    # (§9-1 "로그아웃 시 서버 측 즉시 토큰 무효화 미구현" 해소, `app/core/token_blacklist.py`).
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
        "jti": str(uuid.uuid4()),
    }
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
    """토큰을 검증·디코드한다. 서명/만료/타입이 올바르지 않거나 로그아웃 등으로 블랙리스트에
    등록된 토큰이면 `TokenError`를 발생시킨다 — `get_current_user`(액세스 토큰)와
    `POST /auth/refresh`(리프레시 토큰) 양쪽이 이 함수 하나만 거치므로, 블랙리스트 검사를
    여기 한 곳에 두면 두 경로 모두 자동으로 적용된다."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise TokenError("유효하지 않거나 만료된 토큰입니다.") from exc

    if payload.get("type") != expected_type:
        raise TokenError("토큰 종류가 올바르지 않습니다.")
    if is_blacklisted(payload.get("jti", "")):
        raise TokenError("로그아웃 처리된 토큰입니다.")
    return payload
