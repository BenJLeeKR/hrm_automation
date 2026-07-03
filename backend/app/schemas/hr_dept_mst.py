import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
