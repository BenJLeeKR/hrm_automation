import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.models.hr_empl_mst import EMPL_STAT_CODES
from app.schemas.pagination import PaginatedResponse

EmplStatCd = Literal[EMPL_STAT_CODES]  # type: ignore[valid-type]


class EmployeeCreate(BaseModel):
    """사원 등록 요청 스키마 (`POST /api/v1/employees`)"""

    EMPL_NO: str
    EMPL_NM: str
    DEPT_ID: uuid.UUID
    JIKGUP_ID: uuid.UUID
    JIKMU_ID: uuid.UUID | None = None
    EMPL_STAT_CD: EmplStatCd = "ACTIVE"
    # NOT NULL (2026-07-06 설계 확정, §8 큐 1-1) — 등록 즉시 이메일로 SYS_USER_MST 계정을
    # 자동 생성하는 사원-계정 연동 설계 때문에 필수값으로 전환(§8 큐 1-2에서 계정 자동
    # 생성 로직을 구현한다 — 이 스키마 변경은 그 전제조건인 필수 입력만 다룬다).
    EMAIL_ADDR: str
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
    EMAIL_ADDR: str
    MPHONE_NO: str | None
    HIRE_DT: date | None
    RETIR_DT: date | None
    REG_DTTM: datetime
    UPD_DTTM: datetime


class EmployeeCreateOut(EmployeeOut):
    """사원 등록 응답 스키마 (`POST /api/v1/employees`, §8 큐 1-2 "사원 계정 자동 생성") —
    `EmployeeOut`에 발급된 임시 비밀번호를 추가로 담는다. 이메일 발송 인프라가 없어
    (설계서 §5.5·§9 리스크 참조) 이 응답에 평문으로 1회만 노출하고 서버에는 해시만
    저장한다 — 등록자가 화면에서 확인 후 신규 사원에게 직접 전달해야 한다."""

    temp_password: str


EmployeeListResponse = PaginatedResponse[EmployeeOut]
"""사원 목록 조회 응답 — 공통 페이지네이션 스키마(`app/schemas/pagination.py`) 재사용."""
