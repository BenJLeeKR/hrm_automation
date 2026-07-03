"""create HR_EMPL_ROLE_REL table (Phase 2 후속, ERD §3.6-1)

스키마 근거: backend/docs/ERD.md §3.6-1 — 사원역할 연결 N:M 테이블(복수 직무 지원,
2026-07-02 관계자 확인으로 Phase 2 범위 포함 확정).

이전 리비전들과 동일하게 로컬 환경에 alembic 패키지가 없어 `alembic revision
--autogenerate`로 생성하지 못하고 app/models/hr_empl_role_rel.py의 SQLAlchemy 모델
정의를 기준으로 수기 작성했다. 실 DB에 대한 `alembic upgrade head` 적용 검증은 아직
수행하지 못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: ca8a45d7771f
Revises: ea8f648e460f
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ca8a45d7771f"
down_revision: Union[str, None] = "ea8f648e460f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "HR_EMPL_ROLE_REL",
        sa.Column("EMPL_ROLE_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False),
        sa.Column("JIKMU_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_JIKMU_MST.JIKMU_ID"), nullable=False),
        sa.Column("IS_PRIMARY", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("EMPL_ID", "JIKMU_ID", name="uq_hr_empl_role_rel_empl_jikmu"),
    )


def downgrade() -> None:
    op.drop_table("HR_EMPL_ROLE_REL")
