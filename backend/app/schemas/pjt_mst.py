import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.models.pjt_mst import PJT_STAT_CODES

PjtStatCd = Literal[PJT_STAT_CODES]  # type: ignore[valid-type]


class ProjectCreate(BaseModel):
    """프로젝트 등록 요청 스키마 (`POST /api/v1/projects`)"""

    PJT_CD: str
    PJT_NM: str
    CLNT_NM: str | None = None
    PJT_STAT_CD: PjtStatCd = "PLANNED"
    STRT_DT: date
    END_DT: date | None = None
    PJT_DESC: str | None = None


class ProjectUpdate(BaseModel):
    """프로젝트 수정 요청 스키마 (`PATCH /api/v1/projects/{pjt_id}`) — 전달된 필드만 갱신한다."""

    PJT_CD: str | None = None
    PJT_NM: str | None = None
    CLNT_NM: str | None = None
    PJT_STAT_CD: PjtStatCd | None = None
    STRT_DT: date | None = None
    END_DT: date | None = None
    PJT_DESC: str | None = None


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


class ProjectListResponse(BaseModel):
    """프로젝트 목록 조회 응답 — 공통 페이지네이션 처리(로드맵 §11 "페이지네이션 공통 처리 구현")는
    Phase 3 후속 작업 예정이라, `employees.py`와 동일하게 skip/limit 기반 최소 형태로 구현한다."""

    total: int
    skip: int
    limit: int
    items: list[ProjectOut]
