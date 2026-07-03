import uuid

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class HrEmplRoleRel(TimestampMixin, Base):
    """사원역할 연결 — N:M 연결 테이블 (ERD `backend/docs/ERD.md` §3.6-1)

    사원의 복수 보유역할을 관리한다. `HR_EMPL_MST.JIKMU_ID`가 주(Primary) 직무 1개를
    나타내는 반면, 이 테이블은 "PM, AA"처럼 복수 역할을 보유한 경우를 처리한다.

    `IS_PRIMARY=TRUE`인 행의 JIKMU_ID가 HR_EMPL_MST.JIKMU_ID와 일치해야 한다는 규칙은
    설계서 §5.5에 따라 DB 제약이 아닌 애플리케이션(서비스) 레이어에서 보장한다 (Phase 3).
    """

    __tablename__ = "HR_EMPL_ROLE_REL"
    __table_args__ = (UniqueConstraint("EMPL_ID", "JIKMU_ID", name="uq_hr_empl_role_rel_empl_jikmu"),)

    EMPL_ROLE_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMPL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False)
    JIKMU_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_JIKMU_MST.JIKMU_ID"), nullable=False)
    IS_PRIMARY: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
