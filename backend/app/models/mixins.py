from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """REG_DTTM/UPD_DTTM만 갖는 테이블(HR_DEPT_MST, HR_JIKGUP_MST, HR_JIKMU_MST,
    HR_SKILL_MST 등 마스터 테이블)에서 공통으로 사용."""

    REG_DTTM: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    UPD_DTTM: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class AuditMixin(TimestampMixin):
    """REG_USER/UPD_USER까지 갖는 테이블(HR_EMPL_MST, PJT_MST, PJT_ASGN_HIS 등
    업무 트랜잭션 테이블)에서 사용."""

    REG_USER: Mapped[str | None] = mapped_column(String(100), nullable=True)
    UPD_USER: Mapped[str | None] = mapped_column(String(100), nullable=True)
