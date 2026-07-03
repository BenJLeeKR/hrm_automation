import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
