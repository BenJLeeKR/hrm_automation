import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogOut(BaseModel):
    """감사 로그 조회 응답 스키마 (ERD `backend/docs/ERD.md` §3.14, `SYS_AUDIT_LOG` 컬럼 기준)

    `BFR_VAL_JSON`/`AFT_VAL_JSON`에 담긴 JWT·비밀번호·API 키 등 민감정보 마스킹은 설계서
    §11에 따라 기록 시점(감사 로그 미들웨어, Phase 3)에 처리하며, 이 스키마는 이미 마스킹된
    값을 그대로 조회 응답으로 전달하는 것을 전제로 한다.
    """

    model_config = ConfigDict(from_attributes=True)

    AUDIT_ID: uuid.UUID
    USER_ID: uuid.UUID
    ACT_CD: str
    TGT_TBL_NM: str
    TGT_ID: uuid.UUID | None
    BFR_VAL_JSON: dict | None
    AFT_VAL_JSON: dict | None
    CLNT_IP: str | None
    USER_AGT: str | None
    REG_DTTM: datetime
