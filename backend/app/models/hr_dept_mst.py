import uuid

from sqlalchemy import Boolean, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class HrDeptMst(TimestampMixin, Base):
    """부서 마스터 (ERD `backend/docs/ERD.md` §3.1)"""

    __tablename__ = "HR_DEPT_MST"

    DEPT_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    DEPT_CD: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    DEPT_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    PRNT_DEPT_ID: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("HR_DEPT_MST.DEPT_ID"), nullable=True
    )
    DEPT_ORD: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default="0")
    USE_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
