import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import AuditMixin

PJT_STAT_CODES = ("PLANNED", "RUNNING", "CLOSED", "HOLD")


class PjtMst(AuditMixin, Base):
    """프로젝트 마스터 (ERD `backend/docs/ERD.md` §3.8)"""

    __tablename__ = "PJT_MST"
    __table_args__ = (CheckConstraint(f"PJT_STAT_CD IN {PJT_STAT_CODES}", name="ck_pjt_mst_pjt_stat_cd"),)

    PJT_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    PJT_CD: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    PJT_NM: Mapped[str] = mapped_column(String(200), nullable=False)
    CLNT_NM: Mapped[str | None] = mapped_column(String(200), nullable=True)
    PJT_STAT_CD: Mapped[str] = mapped_column(String(20), nullable=False)
    STRT_DT: Mapped[date] = mapped_column(Date, nullable=False)
    END_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
    PJT_DESC: Mapped[str | None] = mapped_column(Text, nullable=True)
