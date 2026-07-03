import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ResourceRequestOut(BaseModel):
    """리소스 요청 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.10, `PJT_RSRC_REQ` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    REQ_ID: uuid.UUID
    PJT_ID: uuid.UUID
    REQ_USER_ID: uuid.UUID
    REQ_JIKMU_ID: uuid.UUID | None
    REQ_ROLE_NM: str
    REQ_SKILL_JSON: dict
    MIN_ALLOC_RT: int
    REQ_AVAIL_DT: date
    REQ_HC: int
    REQ_STAT_CD: str
    RMRK: str | None
    REG_DTTM: datetime
    REG_USER: str | None
    UPD_DTTM: datetime
    UPD_USER: str | None
