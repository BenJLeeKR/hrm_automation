import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class HrSkillMst(TimestampMixin, Base):
    """기술 마스터 (ERD `backend/docs/ERD.md` §3.4, MVP Seed 초안 `app/db/seed/hr_skill_mst_seed.py`)"""

    __tablename__ = "HR_SKILL_MST"

    SKILL_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # SKILL_GRP_CD는 ERD상 예시 카테고리(BACKEND/FRONTEND/DB/CLOUD 등)로 열거되어 있으나
    # 닫힌 Enum으로 명시되어 있지 않아 CHECK 제약을 두지 않음 (운영팀 확정 전 그룹 추가 여지)
    SKILL_GRP_CD: Mapped[str] = mapped_column(String(50), nullable=False)
    SKILL_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    USE_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
