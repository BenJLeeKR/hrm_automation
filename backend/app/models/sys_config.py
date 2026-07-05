from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SysConfig(Base):
    """시스템 설정 — 키/값 (ERD `backend/docs/ERD.md` §3.16, 설계서 §5.3.17, 2026-07-05 신규)

    코드베이스 내 유일하게 `CONFIG_KEY`(VARCHAR)를 PK로 쓰는 테이블이다 — 다른 테이블은
    전부 UUID PK를 쓰지만, 이 테이블은 사람이 읽을 수 있는 고정 키(`notification.*`)로
    직접 조회/갱신하는 용도라 UUID가 불필요하다. FK 관계 없는 독립 테이블.
    """

    __tablename__ = "SYS_CONFIG"

    CONFIG_KEY: Mapped[str] = mapped_column(String(100), primary_key=True)
    CONFIG_GRP: Mapped[str] = mapped_column(String(50), nullable=False)
    CONFIG_NM: Mapped[str] = mapped_column(String(200), nullable=False)
    CONFIG_VAL: Mapped[str | None] = mapped_column(Text, nullable=True)
    IS_SECRET: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    CONFIG_DESC: Mapped[str | None] = mapped_column(Text, nullable=True)
    UPD_DTTM: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    UPD_USER: Mapped[str | None] = mapped_column(String(100), nullable=True)
