import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class EmployeeSkillOut(BaseModel):
    """사원기술 연결 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.6, `HR_EMPL_SKILL_REL` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    EMPL_SKILL_ID: uuid.UUID
    EMPL_ID: uuid.UUID
    SKILL_ID: uuid.UUID
    PRFCY_LEVL: int | None
    EXPR_YEAR: float | None
    LAST_USE_DT: date | None
    RMRK: str | None
    REG_DTTM: datetime
    UPD_DTTM: datetime
