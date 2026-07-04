import re
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

# 비밀번호 정책 (SCR-015 "유효성 검사" — 8자 이상, 영문·숫자·특수문자 포함)
_PASSWORD_MIN_LENGTH = 8
_PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$")


class UserCreate(BaseModel):
    """시스템 사용자 등록 요청 스키마 (`POST /api/v1/users`, SCR-015 "계정 등록/수정 모달")"""

    USER_LGID: str
    EMAIL_ADDR: str
    password: str
    ROLE_ID: uuid.UUID
    EMPL_ID: uuid.UUID | None = None
    USE_YN: bool = True

    @field_validator("password")
    @classmethod
    def _validate_password(cls, value: str) -> str:
        if len(value) < _PASSWORD_MIN_LENGTH or not _PASSWORD_PATTERN.match(value):
            raise ValueError("8자 이상, 영문·숫자·특수문자를 포함해야 합니다.")
        return value


class SysUserOut(BaseModel):
    """시스템 사용자 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.12, `SYS_USER_MST` 컬럼 기준)

    `ENCR_PWD`(암호화 비밀번호)는 해시값이라도 API 응답에 노출하지 않는다 — 설계서 §11
    보안 요건과 동일한 원칙으로 이 스키마에서 의도적으로 제외한다.
    """

    model_config = ConfigDict(from_attributes=True)

    USER_ID: uuid.UUID
    EMPL_ID: uuid.UUID | None
    USER_LGID: str
    EMAIL_ADDR: str
    ROLE_ID: uuid.UUID
    USE_YN: bool
    LAST_LGN_DTTM: datetime | None
    REG_DTTM: datetime
    UPD_DTTM: datetime
