"""create PJT_RSRC_REQ table (Phase 2 후속, ERD §3.10)

스키마 근거: backend/docs/ERD.md §3.10 — 리소스 요청.

이전 리비전들과 동일하게 로컬 환경에 alembic 패키지가 없어 `alembic revision
--autogenerate`로 생성하지 못하고 app/models/pjt_rsrc_req.py의 SQLAlchemy 모델
정의를 기준으로 수기 작성했다. 실 DB에 대한 `alembic upgrade head` 적용 검증은 아직
수행하지 못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: afbd73237178
Revises: 611b8a04d673
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "afbd73237178"
down_revision: Union[str, None] = "611b8a04d673"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "PJT_RSRC_REQ",
        sa.Column("REQ_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("PJT_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("PJT_MST.PJT_ID"), nullable=False),
        sa.Column(
            "REQ_USER_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("SYS_USER_MST.USER_ID"), nullable=False
        ),
        sa.Column(
            "REQ_JIKMU_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_JIKMU_MST.JIKMU_ID"), nullable=True
        ),
        sa.Column("REQ_ROLE_NM", sa.String(100), nullable=False),
        sa.Column("REQ_SKILL_JSON", postgresql.JSONB, nullable=False),
        sa.Column("MIN_ALLOC_RT", sa.SmallInteger, nullable=False),
        sa.Column("REQ_AVAIL_DT", sa.Date, nullable=False),
        sa.Column("REQ_HC", sa.SmallInteger, nullable=False, server_default="1"),
        sa.Column("REQ_STAT_CD", sa.String(20), nullable=False),
        sa.Column("RMRK", sa.Text, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("REG_USER", sa.String(100), nullable=True),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_USER", sa.String(100), nullable=True),
        sa.CheckConstraint(
            '"REQ_STAT_CD" IN (\'OPEN\', \'IN_REVIEW\', \'FULFILLED\', \'CANCELED\')',
            name="ck_pjt_rsrc_req_req_stat_cd",
        ),
    )


def downgrade() -> None:
    op.drop_table("PJT_RSRC_REQ")
