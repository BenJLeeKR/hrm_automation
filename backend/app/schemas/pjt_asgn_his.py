import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.pjt_asgn_his import ASGN_STAT_CODES, ASGN_TYPE_CODES
from app.schemas.pagination import PaginatedResponse

AsgnTypeCd = Literal[ASGN_TYPE_CODES]  # type: ignore[valid-type]
AsgnStatCd = Literal[ASGN_STAT_CODES]  # type: ignore[valid-type]


class AssignmentCreate(BaseModel):
    """투입 이력 등록 요청 스키마 (`POST /api/v1/assignments`)

    `ALLOC_RT`는 ERD `PJT_ASGN_HIS` CHECK 제약(0~100)과 동일한 범위로 검증한다.
    """

    EMPL_ID: uuid.UUID
    PJT_ID: uuid.UUID
    ASGN_TYPE_CD: AsgnTypeCd = "RUNNING"
    PRJT_ROLE_NM: str
    ALLOC_RT: int = Field(ge=0, le=100)
    ASGN_STRT_DT: date
    ASGN_END_DT: date | None = None
    ASGN_STAT_CD: AsgnStatCd = "PLANNED"
    RMRK: str | None = None


class AssignmentUpdate(BaseModel):
    """투입 이력 수정 요청 스키마 (`PATCH /api/v1/assignments/{asgn_id}`) — 전달된 필드만 갱신한다."""

    ASGN_TYPE_CD: AsgnTypeCd | None = None
    PRJT_ROLE_NM: str | None = None
    ALLOC_RT: int | None = Field(default=None, ge=0, le=100)
    ASGN_STRT_DT: date | None = None
    ASGN_END_DT: date | None = None
    ASGN_STAT_CD: AsgnStatCd | None = None
    RMRK: str | None = None


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


AssignmentListResponse = PaginatedResponse[AssignmentOut]
"""투입 이력 목록 조회 응답 — 공통 페이지네이션 스키마(`app/schemas/pagination.py`) 재사용."""
