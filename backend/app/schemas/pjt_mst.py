import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ProjectOut(BaseModel):
    """프로젝트 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.8, `PJT_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    PJT_ID: uuid.UUID
    PJT_CD: str
    PJT_NM: str
    CLNT_NM: str | None
    PJT_STAT_CD: str
    STRT_DT: date
    END_DT: date | None
    PJT_DESC: str | None
    REG_DTTM: datetime
    REG_USER: str | None
    UPD_DTTM: datetime
    UPD_USER: str | None
