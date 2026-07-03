import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SysBatchHis(Base):
    """배치 실행 이력 (ERD `backend/docs/ERD.md` §3.15)

    ERD상 이 테이블만 유일하게 제약(NOT NULL 등) 표기가 전혀 없는 3열 구조(컬럼명/타입/설명)로
    정의되어 있어, BATCH_ID(PK)를 제외한 모든 컬럼을 nullable로 구현한다. FK 관계 없는
    독립 테이블이며, REG_DTTM만 있고 UPD_DTTM이 없어 다른 Mixin 없이 직접 선언한다
    (SysAuditLog/HrAvailSnap/PjtRcmdRslt와 동일 패턴).

    실제 배치(HR_AVAIL_SNAP_GEN 등 Phase 7 배치 5종)의 실행/기록 로직은 Phase 7에서
    구현하며, 이 모델은 컬럼 정의만 다룬다.
    """

    __tablename__ = "SYS_BATCH_HIS"

    BATCH_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    BATCH_NM: Mapped[str | None] = mapped_column(String(100), nullable=True)
    EXEC_STAT_CD: Mapped[str | None] = mapped_column(String(20), nullable=True)
    EXEC_STRT_DTTM: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    EXEC_END_DTTM: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    RSLT_SUMR: Mapped[str | None] = mapped_column(Text, nullable=True)
    ERR_MSG: Mapped[str | None] = mapped_column(Text, nullable=True)
    CRT_CNT: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UPD_CNT: Mapped[int | None] = mapped_column(Integer, nullable=True)
    FAIL_CNT: Mapped[int | None] = mapped_column(Integer, nullable=True)
    REG_DTTM: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
