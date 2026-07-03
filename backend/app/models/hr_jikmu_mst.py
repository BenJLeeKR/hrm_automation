import uuid

from sqlalchemy import Boolean, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class HrJikmuMst(TimestampMixin, Base):
    """직무 마스터 (ERD `backend/docs/ERD.md` §3.3, Seed 12건 — Phase 2 §8-6 예정)"""

    __tablename__ = "HR_JIKMU_MST"

    JIKMU_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    JIKMU_CD: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    JIKMU_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    JIKMU_GRP_CD: Mapped[str | None] = mapped_column(String(50), nullable=True)
    JIKMU_DESC: Mapped[str | None] = mapped_column(Text, nullable=True)
    SORT_ORD: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default="0")
    USE_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
