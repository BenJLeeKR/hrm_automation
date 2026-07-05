import uuid

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """로그인 요청 스키마 (`POST /api/v1/auth/login`)"""

    USER_LGID: str
    password: str


class TokenResponse(BaseModel):
    """로그인 성공 응답 — 액세스/리프레시 토큰 한 쌍을 발급한다."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """토큰 갱신 요청 스키마 (`POST /api/v1/auth/refresh`)"""

    refresh_token: str


class AccessTokenResponse(BaseModel):
    """토큰 갱신 응답 — 리프레시 토큰은 재발급하지 않고 액세스 토큰만 갱신한다."""

    access_token: str
    token_type: str = "bearer"


class MeOut(BaseModel):
    """현재 로그인 사용자 정보 응답 (`GET /api/v1/auth/me`) — 프론트엔드가 화면 접근 권한
    (`PERM_JSON`)을 조회해 메뉴를 필터링하는 데 사용한다 (로드맵 §8 "권한별 메뉴 제어")."""

    USER_ID: uuid.UUID
    USER_LGID: str
    EMAIL_ADDR: str
    ROLE_CD: str
    ROLE_NM: str
    PERM_JSON: dict | None


class MeUpdate(BaseModel):
    """본인 정보 수정 요청 (`PATCH /api/v1/auth/me`, §9-1 "내 프로필" 화면). 로그인 사용자가
    직접 수정할 수 있는 필드만 노출한다 — 로그인 ID(`USER_LGID`)·역할(`ROLE_ID`)은 관리자용
    사용자 관리(SCR-015, `PATCH /users/{user_id}`)에서만 변경 가능하며 본인 수정 대상이 아니다."""

    EMAIL_ADDR: str | None = None
