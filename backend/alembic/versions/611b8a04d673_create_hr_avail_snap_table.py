"""create HR_AVAIL_SNAP table (Phase 2 후속, ERD §3.7)

스키마 근거: backend/docs/ERD.md §3.7 — 가동가능 스냅샷. 산정 로직은
backend/docs/AVAILABILITY_CALC_SPEC.md 참조 (실제 계산 배치는 Phase 7 구현 예정,
이 리비전은 테이블 스키마만 다룬다).

이전 리비전들과 동일하게 로컬 환경에 alembic 패키지가 없어 `alembic revision
--autogenerate`로 생성하지 못하고 app/models/hr_avail_snap.py의 SQLAlchemy 모델
정의를 기준으로 수기 작성했다. 실 DB에 대한 `alembic upgrade head` 적용 검증은 아직
수행하지 못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: 611b8a04d673
Revises: ca8a45d7771f
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "611b8a04d673"
down_revision: Union[str, None] = "ca8a45d7771f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "HR_AVAIL_SNAP",
        sa.Column("SNAP_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False),
        sa.Column("SNAP_DT", sa.Date, nullable=False),
        sa.Column("TOT_ALLOC_RT", sa.SmallInteger, nullable=False),
        sa.Column("AVAIL_RT", sa.SmallInteger, nullable=False),
        sa.Column("AVAIL_STRT_DT", sa.Date, nullable=True),
        sa.Column("AVAIL_STAT_CD", sa.String(20), nullable=False),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            '"AVAIL_STAT_CD" IN (\'AVAILABLE\', \'PARTIAL\', \'FULL\')', name="ck_hr_avail_snap_avail_stat_cd"
        ),
    )


def downgrade() -> None:
    op.drop_table("HR_AVAIL_SNAP")
