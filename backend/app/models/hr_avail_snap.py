import uuid
from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, SmallInteger, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

AVAIL_STAT_CODES = ("AVAILABLE", "PARTIAL", "FULL")


class HrAvailSnap(Base):
    """가동가능 스냅샷 (ERD `backend/docs/ERD.md` §3.7)

    ERD상 REG_DTTM만 있고 UPD_DTTM이 없어(매일 배치로 생성되는 append-only 스냅샷 성격)
    다른 Mixin을 사용하지 않고 REG_DTTM만 직접 선언한다 (SysAuditLog와 동일 패턴).

    AVAIL_STRT_DT 산정 로직(투입률 0%=오늘, <100%=부분, >=100%=MAX(ASGN_END_DT)+1일)은
    `backend/docs/AVAILABILITY_CALC_SPEC.md`에 정의되어 있으며, 실제 계산은 매일 01:00
    실행되는 배치 `HR_AVAIL_SNAP_GEN`(Phase 7)에서 수행한다 — 이 모델은 컬럼 정의만 다룬다.
    """

    __tablename__ = "HR_AVAIL_SNAP"
    # CHECK 조건문의 컬럼명은 큰따옴표로 감싸야 한다 — hr_empl_mst.py 주석 참조
    # (따옴표 없이 쓰면 Postgres가 대소문자를 소문자로 접어 컬럼을 못 찾는다)
    __table_args__ = (CheckConstraint(f'"AVAIL_STAT_CD" IN {AVAIL_STAT_CODES}', name="ck_hr_avail_snap_avail_stat_cd"),)

    SNAP_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMPL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False)
    SNAP_DT: Mapped[date] = mapped_column(Date, nullable=False)
    TOT_ALLOC_RT: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    AVAIL_RT: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    AVAIL_STRT_DT: Mapped[date | None] = mapped_column(Date, nullable=True)
    AVAIL_STAT_CD: Mapped[str] = mapped_column(String(20), nullable=False)
    REG_DTTM: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
