import uuid

from pydantic import BaseModel, field_validator

from app.schemas.sys_user_mst import _PASSWORD_MIN_LENGTH, _PASSWORD_PATTERN


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


class LogoutRequest(BaseModel):
    """로그아웃 요청 스키마 (`POST /api/v1/auth/logout`, §9-1 "로그아웃 시 서버 측 즉시 토큰
    무효화 미구현" 해소). `refresh_token`은 선택 — 함께 전달하면 액세스 토큰과 함께
    블랙리스트에 등록해 리프레시로 새 액세스 토큰을 재발급받는 것도 막는다. 생략 시
    액세스 토큰만 무효화되며 기존 리프레시 토큰은 자연 만료까지 유효하다."""

    refresh_token: str | None = None


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


class ChangePasswordRequest(BaseModel):
    """비밀번호 변경 요청 (`POST /api/v1/auth/change-password`, 설계서 §6 API 목록에 이미
    명시되어 있던 엔드포인트, §9-1 "설정" 메뉴를 "비밀번호 변경"으로 교체). 현재 비밀번호
    확인 후 새 비밀번호로 교체한다 — `SYS_USER_MST.PWD_CHG_YN`(최초 로그인 강제 변경) 연동은
    해당 컬럼이 아직 없어(로드맵 §8 큐 2번 "사원-계정 연동" 마이그레이션 대기 중) 이번
    범위에서 다루지 않는다."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def _validate_new_password(cls, value: str) -> str:
        if len(value) < _PASSWORD_MIN_LENGTH or not _PASSWORD_PATTERN.match(value):
            raise ValueError("8자 이상, 영문·숫자·특수문자를 포함해야 합니다.")
        return value
