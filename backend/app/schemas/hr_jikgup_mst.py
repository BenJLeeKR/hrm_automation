import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PositionCreate(BaseModel):
    """직급 등록 요청 스키마 (`POST /api/v1/positions`, 설계서 §6.4 "부서/직급 코드" — 전용
    관리 화면 없이 Admin이 `/docs`(Swagger UI)에서 직접 호출하는 용도)"""

    JIKGUP_CD: str
    JIKGUP_NM: str
    JIKGUP_ORD: int
    USE_YN: bool = True


class PositionUpdate(BaseModel):
    """직급 수정 요청 스키마 (`PATCH /api/v1/positions/{jikgup_id}`) — 전달된 필드만 갱신한다.
    `USE_YN=FALSE` 요청은 해당 직급의 재직(`EMPL_STAT_CD='ACTIVE'`) 사원이 있으면 409로
    거부한다(설계서 §5.5 "직급 비활성 보호")."""

    JIKGUP_CD: str | None = None
    JIKGUP_NM: str | None = None
    JIKGUP_ORD: int | None = None
    USE_YN: bool | None = None


class PositionOut(BaseModel):
    """직급 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.2, `HR_JIKGUP_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    JIKGUP_ID: uuid.UUID
    JIKGUP_CD: str
    JIKGUP_NM: str
    JIKGUP_ORD: int
    USE_YN: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
