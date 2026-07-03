"""create SYS_USER_MST/SYS_ROLE_MST/SYS_AUDIT_LOG tables + SYS_ROLE_MST seed (Phase 2, §8 다음 작업 6번)

스키마 근거: backend/docs/ERD.md §3.12~3.14.
Seed 근거: backend/app/db/seed/sys_role_mst_seed.py (MVP 확정, 2026-07-02) — 이 리비전에서
직접 목록을 재작성하지 않고 해당 모듈을 import해 재사용한다.

이 리비전도 이전 리비전(28ce52377e32)과 동일하게 로컬 환경에 alembic 패키지가 없어
`alembic revision --autogenerate`로 생성하지 못하고 app/models/의 SQLAlchemy 모델 정의를
기준으로 수기 작성했다. 실 DB에 대한 `alembic upgrade head` 적용 검증은 아직 수행하지
못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: 83fc676b952e
Revises: 28ce52377e32
Create Date: 2026-07-03

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from app.db.seed.sys_role_mst_seed import SYS_ROLE_MST_SEED

# revision identifiers, used by Alembic.
revision: str = "83fc676b952e"
down_revision: Union[str, None] = "28ce52377e32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "SYS_ROLE_MST",
        sa.Column("ROLE_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("ROLE_CD", sa.String(50), nullable=False, unique=True),
        sa.Column("ROLE_NM", sa.String(100), nullable=False),
        sa.Column("ROLE_DESC", sa.Text, nullable=True),
        sa.Column("PERM_JSON", postgresql.JSONB, nullable=True),
        sa.Column("USE_YN", sa.Boolean, nullable=False, server_default="true"),
    )

    op.create_table(
        "SYS_USER_MST",
        sa.Column("USER_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=True),
        sa.Column("USER_LGID", sa.String(100), nullable=False, unique=True),
        sa.Column("EMAIL_ADDR", sa.String(255), nullable=False, unique=True),
        sa.Column("ENCR_PWD", sa.String(255), nullable=True),
        sa.Column("ROLE_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("SYS_ROLE_MST.ROLE_ID"), nullable=False),
        sa.Column("USE_YN", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("LAST_LGN_DTTM", sa.DateTime(timezone=True), nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "SYS_AUDIT_LOG",
        sa.Column("AUDIT_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("USER_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("SYS_USER_MST.USER_ID"), nullable=False),
        sa.Column("ACT_CD", sa.String(50), nullable=False),
        sa.Column("TGT_TBL_NM", sa.String(100), nullable=False),
        sa.Column("TGT_ID", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("BFR_VAL_JSON", postgresql.JSONB, nullable=True),
        sa.Column("AFT_VAL_JSON", postgresql.JSONB, nullable=True),
        sa.Column("CLNT_IP", sa.String(45), nullable=True),
        sa.Column("USER_AGT", sa.Text, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # SYS_ROLE_MST Seed (6종, MVP 확정) — app/db/seed/sys_role_mst_seed.py 재사용
    sys_role_mst = sa.table(
        "SYS_ROLE_MST",
        sa.column("ROLE_ID", postgresql.UUID(as_uuid=True)),
        sa.column("ROLE_CD", sa.String),
        sa.column("ROLE_NM", sa.String),
        sa.column("ROLE_DESC", sa.Text),
        sa.column("PERM_JSON", postgresql.JSONB),
    )
    op.bulk_insert(
        sys_role_mst,
        [
            {
                "ROLE_ID": uuid.uuid4(),
                "ROLE_CD": row["ROLE_CD"],
                "ROLE_NM": row["ROLE_NM"],
                "ROLE_DESC": row["ROLE_DESC"],
                "PERM_JSON": row["PERM_JSON"],
            }
            for row in SYS_ROLE_MST_SEED
        ],
    )


def downgrade() -> None:
    op.drop_table("SYS_AUDIT_LOG")
    op.drop_table("SYS_USER_MST")
    op.drop_table("SYS_ROLE_MST")
