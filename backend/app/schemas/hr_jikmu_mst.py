import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobTypeOut(BaseModel):
    """직무 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.3, `HR_JIKMU_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    JIKMU_ID: uuid.UUID
    JIKMU_CD: str
    JIKMU_NM: str
    JIKMU_GRP_CD: str | None
    JIKMU_DESC: str | None
    SORT_ORD: int
    USE_YN: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
