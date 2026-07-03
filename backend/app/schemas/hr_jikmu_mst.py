import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobTypeCreate(BaseModel):
    """직무 유형 등록 요청 스키마 (`POST /api/v1/job-types`, SCR-006)"""

    JIKMU_CD: str
    JIKMU_NM: str
    JIKMU_GRP_CD: str | None = None
    JIKMU_DESC: str | None = None
    SORT_ORD: int = 0
    USE_YN: bool = True


class JobTypeUpdate(BaseModel):
    """직무 유형 수정 요청 스키마 (`PATCH /api/v1/job-types/{jikmu_id}`) — 전달된 필드만 갱신한다."""

    JIKMU_CD: str | None = None
    JIKMU_NM: str | None = None
    JIKMU_GRP_CD: str | None = None
    JIKMU_DESC: str | None = None
    SORT_ORD: int | None = None
    USE_YN: bool | None = None


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
