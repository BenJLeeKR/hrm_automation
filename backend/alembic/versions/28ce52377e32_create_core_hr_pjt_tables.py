"""create core HR/PJT tables (Phase 2, §8 다음 작업 5번)

HR_DEPT_MST, HR_JIKGUP_MST, HR_JIKMU_MST, HR_SKILL_MST, HR_EMPL_MST, PJT_MST,
PJT_ASGN_HIS — 스키마 근거: backend/docs/ERD.md §3.1~3.5, 3.8~3.9.

이 리비전은 로컬 환경에 alembic 패키지가 없어 `alembic revision --autogenerate`로
생성하지 못하고, app/models/의 SQLAlchemy 모델 정의를 기준으로 수기 작성했다.
실 DB에 대한 `alembic upgrade head` 적용 검증은 아직 수행하지 못했다 — 로드맵
[BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: 28ce52377e32
Revises:
Create Date: 2026-07-03

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "28ce52377e32"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "HR_DEPT_MST",
        sa.Column("DEPT_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("DEPT_CD", sa.String(30), nullable=False, unique=True),
        sa.Column("DEPT_NM", sa.String(100), nullable=False),
        sa.Column("PRNT_DEPT_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_DEPT_MST.DEPT_ID"), nullable=True),
        sa.Column("DEPT_ORD", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("USE_YN", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "HR_JIKGUP_MST",
        sa.Column("JIKGUP_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("JIKGUP_CD", sa.String(30), nullable=False, unique=True),
        sa.Column("JIKGUP_NM", sa.String(100), nullable=False),
        sa.Column("JIKGUP_ORD", sa.SmallInteger, nullable=False),
        sa.Column("USE_YN", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "HR_JIKMU_MST",
        sa.Column("JIKMU_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("JIKMU_CD", sa.String(50), nullable=False, unique=True),
        sa.Column("JIKMU_NM", sa.String(100), nullable=False),
        sa.Column("JIKMU_GRP_CD", sa.String(50), nullable=True),
        sa.Column("JIKMU_DESC", sa.Text, nullable=True),
        sa.Column("SORT_ORD", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("USE_YN", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "HR_SKILL_MST",
        sa.Column("SKILL_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("SKILL_GRP_CD", sa.String(50), nullable=False),
        sa.Column("SKILL_NM", sa.String(100), nullable=False),
        sa.Column("USE_YN", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "HR_EMPL_MST",
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("EMPL_NO", sa.String(30), nullable=False, unique=True),
        sa.Column("EMPL_NM", sa.String(100), nullable=False),
        sa.Column("DEPT_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_DEPT_MST.DEPT_ID"), nullable=False),
        sa.Column(
            "JIKGUP_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_JIKGUP_MST.JIKGUP_ID"), nullable=False
        ),
        sa.Column("JIKMU_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_JIKMU_MST.JIKMU_ID"), nullable=True),
        sa.Column("EMPL_STAT_CD", sa.String(20), nullable=False),
        sa.Column("EMAIL_ADDR", sa.String(255), nullable=True, unique=True),
        sa.Column("MPHONE_NO", sa.String(50), nullable=True),
        sa.Column("HIRE_DT", sa.Date, nullable=True),
        sa.Column("RETIR_DT", sa.Date, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("REG_USER", sa.String(100), nullable=True),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_USER", sa.String(100), nullable=True),
        sa.CheckConstraint('"EMPL_STAT_CD" IN (\'ACTIVE\', \'LEAVE\', \'RETIRED\')', name="ck_hr_empl_mst_empl_stat_cd"),
    )

    op.create_table(
        "PJT_MST",
        sa.Column("PJT_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("PJT_CD", sa.String(30), nullable=False, unique=True),
        sa.Column("PJT_NM", sa.String(200), nullable=False),
        sa.Column("CLNT_NM", sa.String(200), nullable=True),
        sa.Column("PJT_STAT_CD", sa.String(20), nullable=False),
        sa.Column("STRT_DT", sa.Date, nullable=False),
        sa.Column("END_DT", sa.Date, nullable=True),
        sa.Column("PJT_DESC", sa.Text, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("REG_USER", sa.String(100), nullable=True),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_USER", sa.String(100), nullable=True),
        sa.CheckConstraint(
            '"PJT_STAT_CD" IN (\'PLANNED\', \'RUNNING\', \'CLOSED\', \'HOLD\')', name="ck_pjt_mst_pjt_stat_cd"
        ),
    )

    op.create_table(
        "PJT_ASGN_HIS",
        sa.Column("ASGN_ID", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("EMPL_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("HR_EMPL_MST.EMPL_ID"), nullable=False),
        sa.Column("PJT_ID", postgresql.UUID(as_uuid=True), sa.ForeignKey("PJT_MST.PJT_ID"), nullable=False),
        sa.Column("ASGN_TYPE_CD", sa.String(20), nullable=False, server_default="RUNNING"),
        sa.Column("PRJT_ROLE_NM", sa.String(100), nullable=False),
        sa.Column("ALLOC_RT", sa.SmallInteger, nullable=False),
        sa.Column("ASGN_STRT_DT", sa.Date, nullable=False),
        sa.Column("ASGN_END_DT", sa.Date, nullable=True),
        sa.Column("ASGN_STAT_CD", sa.String(20), nullable=False),
        sa.Column("RMRK", sa.Text, nullable=True),
        sa.Column("REG_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("REG_USER", sa.String(100), nullable=True),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_USER", sa.String(100), nullable=True),
        sa.CheckConstraint('"ALLOC_RT" BETWEEN 0 AND 100', name="ck_pjt_asgn_his_alloc_rt"),
        sa.CheckConstraint(
            '"ASGN_TYPE_CD" IN (\'RUNNING\', \'COMMITTED\', \'PROPOSED\')', name="ck_pjt_asgn_his_asgn_type_cd"
        ),
        sa.CheckConstraint(
            '"ASGN_STAT_CD" IN (\'PLANNED\', \'ACTIVE\', \'DONE\', \'CANCELED\')',
            name="ck_pjt_asgn_his_asgn_stat_cd",
        ),
    )


def downgrade() -> None:
    op.drop_table("PJT_ASGN_HIS")
    op.drop_table("PJT_MST")
    op.drop_table("HR_EMPL_MST")
    op.drop_table("HR_SKILL_MST")
    op.drop_table("HR_JIKMU_MST")
    op.drop_table("HR_JIKGUP_MST")
    op.drop_table("HR_DEPT_MST")
