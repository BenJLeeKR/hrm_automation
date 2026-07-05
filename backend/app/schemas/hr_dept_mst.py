import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DepartmentCreate(BaseModel):
    """부서 등록 요청 스키마 (`POST /api/v1/departments`, 설계서 §6.4 "부서/직급 코드" — 전용
    관리 화면 없이 Admin이 `/docs`(Swagger UI)에서 직접 호출하는 용도)"""

    DEPT_CD: str
    DEPT_NM: str
    PRNT_DEPT_ID: uuid.UUID | None = None
    DEPT_ORD: int = 0
    USE_YN: bool = True


class DepartmentUpdate(BaseModel):
    """부서 수정 요청 스키마 (`PATCH /api/v1/departments/{dept_id}`) — 전달된 필드만 갱신한다.
    `USE_YN=FALSE` 요청은 해당 부서에 재직(`EMPL_STAT_CD='ACTIVE'`) 사원이 있으면 409로
    거부한다(설계서 §5.5 "부서 비활성 보호")."""

    DEPT_CD: str | None = None
    DEPT_NM: str | None = None
    PRNT_DEPT_ID: uuid.UUID | None = None
    DEPT_ORD: int | None = None
    USE_YN: bool | None = None


class DepartmentOut(BaseModel):
    """부서 마스터 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.1, `HR_DEPT_MST` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    DEPT_ID: uuid.UUID
    DEPT_CD: str
    DEPT_NM: str
    PRNT_DEPT_ID: uuid.UUID | None
    DEPT_ORD: int
    USE_YN: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
