import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SkillOut(BaseModel):
    """기술 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.4, `HR_SKILL_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    SKILL_ID: uuid.UUID
    SKILL_GRP_CD: str
    SKILL_NM: str
    USE_YN: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
