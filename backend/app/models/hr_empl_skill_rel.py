import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, SmallInteger, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class HrEmplSkillRel(TimestampMixin, Base):
    """사원기술 연결 — N:M 연결 테이블 (ERD `backend/docs/ERD.md` §3.6)"""

    __tablename__ = "HR_EMPL_SKILL_REL"
    # CHECK 조건문의 컬럼명은 큰따옴표로 감싸야 한다 — hr_empl_mst.py 주석 참조
    # (따옴표 없이 쓰면 Postgres가 대소문자를 소문자로 접어 컬럼을 못 찾는다)
    __table_args__ = (CheckConstraint('"PRFCY_LEVL" BETWEEN 1 AND 5', name="ck_hr_empl_skill_rel_prfcy_levl"),)

    EMPL_SKILL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMPL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False)
    SKILL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_SKILL_MST.SKILL_ID"), nullable=False)
    # ERD상 "CHECK 1~5"만 명시되고 NOT NULL 표기는 없어 nullable로 구현
    PRFCY_LEVL: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    EXPR_YEAR: Mapped[float | None] = mapped_column(Numeric(4, 1), nullable=True)
    LAST_USE_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
    RMRK: Mapped[str | None] = mapped_column(Text, nullable=True)
