import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AvailabilitySnapshotOut(BaseModel):
    """가동가능 스냅샷 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.7, `HR_AVAIL_SNAP` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    SNAP_ID: uuid.UUID
    EMPL_ID: uuid.UUID
    SNAP_DT: date
    TOT_ALLOC_RT: int
    AVAIL_RT: int
    AVAIL_STRT_DT: date | None
    AVAIL_STAT_CD: str
    REG_DTTM: datetime
