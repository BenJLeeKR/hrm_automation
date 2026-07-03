import uuid

from sqlalchemy import Boolean, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class HrJikgupMst(TimestampMixin, Base):
    """직급 마스터 (ERD `backend/docs/ERD.md` §3.2, Seed 10건 — Phase 2 §8-6 예정)"""

    __tablename__ = "HR_JIKGUP_MST"

    JIKGUP_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    JIKGUP_CD: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    JIKGUP_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    JIKGUP_ORD: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    USE_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
