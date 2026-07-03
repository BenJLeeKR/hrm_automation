import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AssignmentOut(BaseModel):
    """투입 이력 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.9, `PJT_ASGN_HIS` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    ASGN_ID: uuid.UUID
    EMPL_ID: uuid.UUID
    PJT_ID: uuid.UUID
    ASGN_TYPE_CD: str
    PRJT_ROLE_NM: str
    ALLOC_RT: int
    ASGN_STRT_DT: date
    ASGN_END_DT: date | None
    ASGN_STAT_CD: str
    RMRK: str | None
    REG_DTTM: datetime
    REG_USER: str | None
    UPD_DTTM: datetime
    UPD_USER: str | None
