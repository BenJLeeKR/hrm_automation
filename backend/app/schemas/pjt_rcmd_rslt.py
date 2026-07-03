import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationResultOut(BaseModel):
    """추천 결과 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.11, `PJT_RCMD_RSLT` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    RCMD_ID: uuid.UUID
    REQ_ID: uuid.UUID
    EMPL_ID: uuid.UUID
    RCMD_RANK: int
    TOT_SCORE: float
    SCORE_DTL_JSON: dict | None
    RCMD_RSN: str | None
    SEL_YN: bool
    REG_DTTM: datetime
