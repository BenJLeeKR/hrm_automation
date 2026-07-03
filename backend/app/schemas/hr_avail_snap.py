import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.models.hr_avail_snap import AVAIL_STAT_CODES

AvailStatCd = Literal[AVAIL_STAT_CODES]  # type: ignore[valid-type]


class AvailabilityCalcOut(BaseModel):
    """가동률 즉시 계산 응답 스키마 (`GET /api/v1/availability/{empl_id}`).

    `AVAILABILITY_CALC_SPEC.md` §2/§4 로직으로 즉시 계산한 결과이며, `HR_AVAIL_SNAP`
    테이블에는 저장하지 않는다 — 매일 01:00 배치 `HR_AVAIL_SNAP_GEN`(Phase 7, 미구현)이
    스냅샷 행 생성을 전담한다.
    """

    EMPL_ID: uuid.UUID
    SNAP_DT: date
    TOT_ALLOC_RT: int
    AVAIL_RT: int
    AVAIL_STRT_DT: date | None
    AVAIL_STAT_CD: AvailStatCd
    DATA_QUALITY_WARNING: bool


class AvailabilitySnapshotOut(BaseModel):
    """가동가능 스냅샷 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.7, `HR_AVAIL_SNAP` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    SNAP_ID: uuid.UUID
    EMPL_ID: uuid.UUID
    SNAP_DT: date
    TOT_ALLOC_RT: int
    AVAIL_RT: int
    AVAIL_STRT_DT: date | None
    AVAIL_STAT_CD: str
    REG_DTTM: datetime
