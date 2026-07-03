import uuid

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SysRoleMst(Base):
    """역할 마스터 (ERD `backend/docs/ERD.md` §3.13, Seed `app/db/seed/sys_role_mst_seed.py`)

    ERD상 REG_DTTM/UPD_DTTM 컬럼이 없어 다른 마스터 테이블과 달리 TimestampMixin을
    사용하지 않는다 (설계서 원본 컬럼 정의 그대로 유지).
    """

    __tablename__ = "SYS_ROLE_MST"

    ROLE_ID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ROLE_CD: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ROLE_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    ROLE_DESC: Mapped[str | None] = mapped_column(Text, nullable=True)
    PERM_JSON: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    USE_YN: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
