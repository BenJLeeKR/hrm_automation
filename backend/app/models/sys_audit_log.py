import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SysAuditLog(Base):
    """감사 로그 (ERD `backend/docs/ERD.md` §3.14)

    ERD상 REG_DTTM만 있고 UPD_DTTM이 없어(로그는 수정되지 않는 append-only 성격) 다른
    Mixin을 사용하지 않고 REG_DTTM만 직접 선언한다. BFR_VAL_JSON/AFT_VAL_JSON에 JWT·
    비밀번호·API 키 등 민감정보를 기록할 때는 마스킹 처리가 필요하다 (설계서 §11) — 실제
    마스킹 로직은 Phase 3 감사 로그 미들웨어 구현 시 처리하며, 이 모델은 컬럼 정의만 다룬다.
    """

    __tablename__ = "SYS_AUDIT_LOG"

    AUDIT_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    USER_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("SYS_USER_MST.USER_ID"), nullable=False)
    ACT_CD: Mapped[str] = mapped_column(String(50), nullable=False)
    TGT_TBL_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    TGT_ID: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    BFR_VAL_JSON: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    AFT_VAL_JSON: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    CLNT_IP: Mapped[str | None] = mapped_column(String(45), nullable=True)
    USER_AGT: Mapped[str | None] = mapped_column(Text, nullable=True)
    REG_DTTM: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
