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
    # CHECK 조건문 안의 컬럼명은 큰따옴표로 감싸야 한다 — SQLAlchemy가 컬럼 자체는
    # "EMPL_STAT_CD"처럼 따옴표를 씌워 생성하지만, CheckConstraint의 원문 SQL 문자열은
    # 따옴표를 자동으로 붙여주지 않아 Postgres가 대소문자를 소문자로 접어(empl_stat_cd)
    # "컬럼 없음" 오류를 낸다.
    __table_args__ = (
        CheckConstraint(f'"EMPL_STAT_CD" IN {EMPL_STAT_CODES}', name="ck_hr_empl_mst_empl_stat_cd"),
    )

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
    # NOT NULL (2026-07-06 설계 확정, §8 큐 1-1) — 등록 즉시 이메일로 SYS_USER_MST 계정을
    # 자동 생성하는 사원-계정 연동 설계 때문에 필수값으로 전환했다. 원래 nullable이었으나
    # (설계서 §5.3.1) 이후 v0.6에서 UNIQUE NOT NULL로 변경되었다.
    EMAIL_ADDR: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    MPHONE_NO: Mapped[str | None] = mapped_column(String(50), nullable=True)
    HIRE_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
    RETIR_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
