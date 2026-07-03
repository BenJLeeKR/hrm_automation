import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SkillCreate(BaseModel):
    """기술 등록 요청 스키마 (`POST /api/v1/skills`)"""

    SKILL_GRP_CD: str
    SKILL_NM: str
    USE_YN: bool = True


class SkillUpdate(BaseModel):
    """기술 수정 요청 스키마 (`PATCH /api/v1/skills/{skill_id}`) — 전달된 필드만 갱신한다."""

    SKILL_GRP_CD: str | None = None
    SKILL_NM: str | None = None
    USE_YN: bool | None = None


class SkillOut(BaseModel):
    """기술 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.4, `HR_SKILL_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    SKILL_ID: uuid.UUID
    SKILL_GRP_CD: str
    SKILL_NM: str
    USE_YN: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
