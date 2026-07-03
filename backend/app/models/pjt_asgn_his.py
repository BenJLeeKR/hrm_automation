import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import AuditMixin

ASGN_TYPE_CODES = ("RUNNING", "COMMITTED", "PROPOSED")
ASGN_STAT_CODES = ("PLANNED", "ACTIVE", "DONE", "CANCELED")


class PjtAsgnHis(AuditMixin, Base):
    """투입 이력 (ERD `backend/docs/ERD.md` §3.9)

    데이터 정합성 규칙(동일 사원 동일 기간 ALLOC_RT 합계 100% 초과 금지 등, ERD §3.9 / 설계서
    §5.5)은 DB 제약만으로 표현할 수 없어 서비스 레이어에서 검증한다 (Phase 3 API 구현 시 처리).
    """

    __tablename__ = "PJT_ASGN_HIS"
    # CHECK 조건문의 컬럼명은 큰따옴표로 감싸야 한다 — hr_empl_mst.py 주석 참조
    # (따옴표 없이 쓰면 Postgres가 대소문자를 소문자로 접어 컬럼을 못 찾는다)
    __table_args__ = (
        CheckConstraint('"ALLOC_RT" BETWEEN 0 AND 100', name="ck_pjt_asgn_his_alloc_rt"),
        CheckConstraint(f'"ASGN_TYPE_CD" IN {ASGN_TYPE_CODES}', name="ck_pjt_asgn_his_asgn_type_cd"),
        CheckConstraint(f'"ASGN_STAT_CD" IN {ASGN_STAT_CODES}', name="ck_pjt_asgn_his_asgn_stat_cd"),
    )

    ASGN_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMPL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False)
    PJT_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("PJT_MST.PJT_ID"), nullable=False)
    ASGN_TYPE_CD: Mapped[str] = mapped_column(String(20), nullable=False, default="RUNNING", server_default="RUNNING")
    PRJT_ROLE_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    ALLOC_RT: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ASGN_STRT_DT: Mapped[date] = mapped_column(Date, nullable=False)
    ASGN_END_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
    ASGN_STAT_CD: Mapped[str] = mapped_column(String(20), nullable=False)
    RMRK: Mapped[str | None] = mapped_column(Text, nullable=True)
