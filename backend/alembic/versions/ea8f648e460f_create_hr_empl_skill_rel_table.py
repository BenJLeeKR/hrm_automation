"""create HR_EMPL_SKILL_REL table (Phase 2 후속, ERD §3.6)

스키마 근거: backend/docs/ERD.md §3.6 — 사원기술 연결 N:M 테이블.

이전 리비전들과 동일하게 로컬 환경에 alembic 패키지가 없어 `alembic revision
--autogenerate`로 생성하지 못하고 app/models/hr_empl_skill_rel.py의 SQLAlchemy 모델
정의를 기준으로 수기 작성했다. 실 DB에 대한 `alembic upgrade head` 적용 검증은 아직
수행하지 못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: ea8f648e460f
Revises: 83fc676b952e
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ea8f648e460f"
down_revision: Union[str, None] = "83fc676b952e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "HR_EMPL_SKILL_REL",
        sa.Column("EMPL_SKILL_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False),
        sa.Column("SKILL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_SKILL_MST.SKILL_ID"), nullable=False),
        sa.Column("PRFCY_LEVL", sa.SmallInteger, nullable=True),
        sa.Column("EXPR_YEAR", sa.Numeric(4, 1), nullable=True),
        sa.Column("LAST_USE_DT", sa.Date, nullable=True),
        sa.Column("RMRK", sa.Text, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint('"PRFCY_LEVL" BETWEEN 1 AND 5', name="ck_hr_empl_skill_rel_prfcy_levl"),
    )


def downgrade() -> None:
    op.drop_table("HR_EMPL_SKILL_REL")
