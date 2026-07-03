import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, SmallInteger, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PjtRcmdRslt(Base):
    """추천 결과 (ERD `backend/docs/ERD.md` §3.11)

    ERD상 REG_DTTM만 있고 UPD_DTTM이 없어(추천 실행 시점 스냅샷 성격, append-only)
    다른 Mixin을 사용하지 않고 REG_DTTM만 직접 선언한다 (SysAuditLog/HrAvailSnap과 동일 패턴).

    추천 점수 산정 가중치(직무 15%+기술 35%+숙련도 25%+가동일 15%+유사경험 7%+역할적합도 3%,
    로드맵 §4 Phase 5/§11 참조)를 반영한 실제 계산 로직은 Phase 5에서 구현하며, 이 모델은
    컬럼 정의만 다룬다.
    """

    __tablename__ = "PJT_RCMD_RSLT"

    RCMD_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    REQ_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("PJT_RSRC_REQ.REQ_ID"), nullable=False)
    EMPL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False)
    RCMD_RANK: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    TOT_SCORE: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    SCORE_DTL_JSON: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    RCMD_RSN: Mapped[str | None] = mapped_column(Text, nullable=True)
    SEL_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    REG_DTTM: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
