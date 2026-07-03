import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PositionOut(BaseModel):
    """직급 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.2, `HR_JIKGUP_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    JIKGUP_ID: uuid.UUID
    JIKGUP_CD: str
    JIKGUP_NM: str
    JIKGUP_ORD: int
    USE_YN: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
