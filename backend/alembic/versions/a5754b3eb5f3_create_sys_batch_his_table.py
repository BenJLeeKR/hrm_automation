"""create SYS_BATCH_HIS table (Phase 2 후속, ERD §3.15)

스키마 근거: backend/docs/ERD.md §3.15 — 배치 실행 이력. ERD상 이 테이블만 유일하게
NOT NULL 등 제약 표기가 전혀 없어 BATCH_ID(PK)를 제외한 전 컬럼을 nullable로 반영했다.
FK 관계 없는 독립 테이블이다.

이 리비전으로 ERD 16개 테이블 전체의 모델·마이그레이션 작성이 완료된다. 이전 리비전들과
동일하게 로컬 환경에 alembic 패키지가 없어 `alembic revision --autogenerate`로 생성하지
못하고 app/models/sys_batch_his.py의 SQLAlchemy 모델 정의를 기준으로 수기 작성했다.
실 DB에 대한 `alembic upgrade head` 적용 검증은 아직 수행하지 못했다 — 로드맵
[BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: a5754b3eb5f3
Revises: 1a7979587160
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a5754b3eb5f3"
down_revision: Union[str, None] = "1a7979587160"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "SYS_BATCH_HIS",
        sa.Column("BATCH_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("BATCH_NM", sa.String(100), nullable=True),
        sa.Column("EXEC_STAT_CD", sa.String(20), nullable=True),
        sa.Column("EXEC_STRT_DTTM", sa.DateTime(timezone=True), nullable=True),
        sa.Column("EXEC_END_DTTM", sa.DateTime(timezone=True), nullable=True),
        sa.Column("RSLT_SUMR", sa.Text, nullable=True),
        sa.Column("ERR_MSG", sa.Text, nullable=True),
        sa.Column("CRT_CNT", sa.Integer, nullable=True),
        sa.Column("UPD_CNT", sa.Integer, nullable=True),
        sa.Column("FAIL_CNT", sa.Integer, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("SYS_BATCH_HIS")
