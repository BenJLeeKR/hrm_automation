import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmployeeRoleOut(BaseModel):
    """사원역할 연결 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.6-1, `HR_EMPL_ROLE_REL` 컬럼 기준)"""

    model_config = ConfigDict(from_attributes=True)

    EMPL_ROLE_ID: uuid.UUID
    EMPL_ID: uuid.UUID
    JIKMU_ID: uuid.UUID
    IS_PRIMARY: bool
    REG_DTTM: datetime
    UPD_DTTM: datetime
