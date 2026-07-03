import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import AuditMixin

REQ_STAT_CODES = ("OPEN", "IN_REVIEW", "FULFILLED", "CANCELED")


class PjtRsrcReq(AuditMixin, Base):
    """리소스 요청 (ERD `backend/docs/ERD.md` §3.10)"""

    __tablename__ = "PJT_RSRC_REQ"
    # CHECK 조건문의 컬럼명은 큰따옴표로 감싸야 한다 — hr_empl_mst.py 주석 참조
    # (따옴표 없이 쓰면 Postgres가 대소문자를 소문자로 접어 컬럼을 못 찾는다)
    __table_args__ = (CheckConstraint(f'"REQ_STAT_CD" IN {REQ_STAT_CODES}', name="ck_pjt_rsrc_req_req_stat_cd"),)

    REQ_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    PJT_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("PJT_MST.PJT_ID"), nullable=False)
    REQ_USER_ID: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("SYS_USER_MST.USER_ID"), nullable=False
    )
    REQ_JIKMU_ID: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("HR_JIKMU_MST.JIKMU_ID"), nullable=True
    )
    REQ_ROLE_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    REQ_SKILL_JSON: Mapped[dict] = mapped_column(JSONB, nullable=False)
    MIN_ALLOC_RT: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    REQ_AVAIL_DT: Mapped[date] = mapped_column(Date, nullable=False)
    REQ_HC: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default="1")
    REQ_STAT_CD: Mapped[str] = mapped_column(String(20), nullable=False)
    RMRK: Mapped[str | None] = mapped_column(Text, nullable=True)
