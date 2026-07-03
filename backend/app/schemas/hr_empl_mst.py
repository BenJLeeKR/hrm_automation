import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.models.hr_empl_mst import EMPL_STAT_CODES

EmplStatCd = Literal[EMPL_STAT_CODES]  # type: ignore[valid-type]


class EmployeeCreate(BaseModel):
    """사원 등록 요청 스키마 (`POST /api/v1/employees`)"""

    EMPL_NO: str
    EMPL_NM: str
    DEPT_ID: uuid.UUID
    JIKGUP_ID: uuid.UUID
    JIKMU_ID: uuid.UUID | None = None
    EMPL_STAT_CD: EmplStatCd = "ACTIVE"
    EMAIL_ADDR: str | None = None
    MPHONE_NO: str | None = None
    HIRE_DT: date | None = None
    RETIR_DT: date | None = None


class EmployeeUpdate(BaseModel):
    """사원 수정 요청 스키마 (`PATCH /api/v1/employees/{empl_id}`) — 전달된 필드만 갱신한다."""

    EMPL_NO: str | None = None
    EMPL_NM: str | None = None
    DEPT_ID: uuid.UUID | None = None
    JIKGUP_ID: uuid.UUID | None = None
    JIKMU_ID: uuid.UUID | None = None
    EMPL_STAT_CD: EmplStatCd | None = None
    EMAIL_ADDR: str | None = None
    MPHONE_NO: str | None = None
    HIRE_DT: date | None = None
    RETIR_DT: date | None = None


class EmployeeOut(BaseModel):
    """사원 목록/상세 응답 스키마 (ERD `backend/docs/ERD.md` §3.5, `HR_EMPL_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    EMPL_ID: uuid.UUID
    EMPL_NO: str
    EMPL_NM: str
    DEPT_ID: uuid.UUID
    JIKGUP_ID: uuid.UUID
    JIKMU_ID: uuid.UUID | None
    EMPL_STAT_CD: str
    EMAIL_ADDR: str | None
    MPHONE_NO: str | None
    HIRE_DT: date | None
    RETIR_DT: date | None
    REG_DTTM: datetime
    UPD_DTTM: datetime


class EmployeeListResponse(BaseModel):
    """사원 목록 조회 응답 — 공통 페이지네이션 처리(로드맵 §11 "페이지네이션 공통 처리 구현")는
    Phase 3 후속 작업 예정이라, 이 엔드포인트는 우선 skip/limit 기반 최소 형태로 구현한다."""

    total: int
    skip: int
    limit: int
    items: list[EmployeeOut]
