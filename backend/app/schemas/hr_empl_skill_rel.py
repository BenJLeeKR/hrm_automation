import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class EmployeeSkillCreate(BaseModel):
    """사원기술 연결 등록 요청 스키마 (`POST /api/v1/employee-skills`)

    `PRFCY_LEVL`은 ERD `HR_EMPL_SKILL_REL` CHECK 제약(1~5)과 동일한 범위로 검증한다.
    """

    EMPL_ID: uuid.UUID
    SKILL_ID: uuid.UUID
    PRFCY_LEVL: int | None = Field(default=None, ge=1, le=5)
    EXPR_YEAR: float | None = None
    LAST_USE_DT: date | None = None
    RMRK: str | None = None


class EmployeeSkillUpdate(BaseModel):
    """사원기술 연결 수정 요청 스키마 (`PATCH /api/v1/employee-skills/{empl_skill_id}`) — 전달된 필드만 갱신한다."""

    PRFCY_LEVL: int | None = Field(default=None, ge=1, le=5)
    EXPR_YEAR: float | None = None
    LAST_USE_DT: date | None = None
    RMRK: str | None = None


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
