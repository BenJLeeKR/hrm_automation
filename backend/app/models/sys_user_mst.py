import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class SysUserMst(TimestampMixin, Base):
    """시스템 사용자 마스터 (ERD `backend/docs/ERD.md` §3.12)

    ENCR_PWD는 bcrypt/argon2 해시만 저장한다 (평문 저장 금지, 설계서 §11) — 실제 해싱 로직은
    Phase 3 인증 API 구현 시 `passlib`로 처리하며, 이 모델은 컬럼 정의만 다룬다.
    """

    __tablename__ = "SYS_USER_MST"

    USER_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMPL_ID: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=True
    )
    USER_LGID: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    EMAIL_ADDR: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    ENCR_PWD: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ROLE_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("SYS_ROLE_MST.ROLE_ID"), nullable=False)
    USE_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    LAST_LGN_DTTM: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
