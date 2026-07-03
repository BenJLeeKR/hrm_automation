"""create PJT_RCMD_RSLT table (Phase 2 후속, ERD §3.11)

스키마 근거: backend/docs/ERD.md §3.11 — 추천 결과. 추천 점수 산정 로직(Phase 5)은
이 리비전 범위 밖이며 테이블 스키마만 다룬다.

이전 리비전들과 동일하게 로컬 환경에 alembic 패키지가 없어 `alembic revision
--autogenerate`로 생성하지 못하고 app/models/pjt_rcmd_rslt.py의 SQLAlchemy 모델
정의를 기준으로 수기 작성했다. 실 DB에 대한 `alembic upgrade head` 적용 검증은 아직
수행하지 못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: 1a7979587160
Revises: afbd73237178
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1a7979587160"
down_revision: Union[str, None] = "afbd73237178"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "PJT_RCMD_RSLT",
        sa.Column("RCMD_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("REQ_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("PJT_RSRC_REQ.REQ_ID"), nullable=False),
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False),
        sa.Column("RCMD_RANK", sa.SmallInteger, nullable=False),
        sa.Column("TOT_SCORE", sa.Numeric(5, 2), nullable=False),
        sa.Column("SCORE_DTL_JSON", postgresql.JSONB, nullable=True),
        sa.Column("RCMD_RSN", sa.Text, nullable=True),
        sa.Column("SEL_YN", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("PJT_RCMD_RSLT")
