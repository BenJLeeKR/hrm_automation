import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import AuditMixin

EMPL_STAT_CODES = ("ACTIVE", "LEAVE", "RETIRED")


class HrEmplMst(AuditMixin, Base):
    """사원 마스터 (ERD `backend/docs/ERD.md` §3.5)"""

    __tablename__ = "HR_EMPL_MST"
    __table_args__ = (CheckConstraint(f"EMPL_STAT_CD IN {EMPL_STAT_CODES}", name="ck_hr_empl_mst_empl_stat_cd"),)

    EMPL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMPL_NO: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    EMPL_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    # DEPT_ID/JIKGUP_ID: ERD상 "FK"로만 표기(JIKMU_ID처럼 "FK NULL"로 명시되지 않음) —
    # 모든 사원은 부서·직급이 있어야 한다는 업무 규칙에 따라 NOT NULL로 구현
    DEPT_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_DEPT_MST.DEPT_ID"), nullable=False)
    JIKGUP_ID: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("HR_JIKGUP_MST.JIKGUP_ID"), nullable=False
    )
    JIKMU_ID: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("HR_JIKMU_MST.JIKMU_ID"), nullable=True
    )
    EMPL_STAT_CD: Mapped[str] = mapped_column(String(20), nullable=False)
    EMAIL_ADDR: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    MPHONE_NO: Mapped[str | None] = mapped_column(String(50), nullable=True)
    HIRE_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
    RETIR_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
