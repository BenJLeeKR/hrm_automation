import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ResourceRequestCreate(BaseModel):
    """리소스 요청 등록 요청 스키마 (`POST /api/v1/resource-requests`, SCR-011 "추천 조건 입력").

    `REQ_SKILL_JSON`은 `{"SKILL_IDS": [...], "MIN_PRFCY_LEVL": 1~5}` 형태를 사용한다 —
    설계서(SCR-011)에 JSON 내부 스키마가 명시되어 있지 않아 "필요 기술"·"최소 숙련도"
    입력 항목을 그대로 담는 MVP 구조로 정의(§9 리스크 참고, 운영팀 확정 전까지 유지).
    """

    PJT_ID: uuid.UUID
    REQ_JIKMU_ID: uuid.UUID | None = None
    REQ_ROLE_NM: str
    REQ_SKILL_JSON: dict = Field(default_factory=dict)
    MIN_ALLOC_RT: int = Field(ge=0, le=100)
    REQ_AVAIL_DT: date
    REQ_HC: int = 1
    RMRK: str | None = None


class ResourceRequestOut(BaseModel):
    """리소스 요청 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.10, `PJT_RSRC_REQ` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    REQ_ID: uuid.UUID
    PJT_ID: uuid.UUID
    REQ_USER_ID: uuid.UUID
    REQ_JIKMU_ID: uuid.UUID | None
    REQ_ROLE_NM: str
    REQ_SKILL_JSON: dict
    MIN_ALLOC_RT: int
    REQ_AVAIL_DT: date
    REQ_HC: int
    REQ_STAT_CD: str
    RMRK: str | None
    REG_DTTM: datetime
    REG_USER: str | None
    UPD_DTTM: datetime
    UPD_USER: str | None
