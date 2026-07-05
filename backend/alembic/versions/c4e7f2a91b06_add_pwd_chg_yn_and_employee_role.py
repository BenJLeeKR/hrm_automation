"""사원-계정 연동 설계 반영 1-1: SYS_USER_MST.PWD_CHG_YN 추가, HR_EMPL_MST.EMAIL_ADDR
NOT NULL 전환, SYS_ROLE_MST에 EMPLOYEE 역할 신규 추가

배경: 로드맵 §8 다음 작업 1번 "사원-계정 연동 설계 반영 — 구현"(2026-07-06 설계 확정,
`[DESIGN]HRM_Automation_System_Design_v0_6.md` §5.3.1/§5.3.9/§5.3.10/§5.5) 1-1 항목.
사원이 본인 계정으로 로그인해 본인 정보를 조회·수정하는 흐름을 지원하기 위한 스키마
변경만 다룬다 — 계정 자동 생성·퇴직 시 계정 비활성화 등 실제 업무 로직은 1-2~1-5에서
후속 구현한다.

`PWD_CHG_YN`: 임시 비밀번호 상태를 나타내는 플래그(기본 TRUE). `EMAIL_ADDR`: 등록 즉시
이메일로 계정을 자동 생성하는 설계 때문에 필수값으로 전환 — 이 리비전 적용 전 이미 NULL인
행이 있으면 안전하게 처리할 수 없어(등록 즉시 자동 생성되는 것이 아니라 사후 보정이 필요)
NOT NULL 제약 추가 전에 남아있는 NULL 값을 사번 기반 placeholder로 먼저 채운다. `EMPLOYEE`
역할은 `app/db/seed/sys_role_mst_seed.py`의 신규 엔트리를 그대로 재사용해 삽입한다
(83fc676b952e가 이미 적용된 상태라 그 리비전을 되돌리지 않고 새 리비전으로 추가).

Revision ID: c4e7f2a91b06
Revises: b1c4d8e29a3f
Create Date: 2026-07-06

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects import postgresql

from alembic import op
from app.db.seed.sys_role_mst_seed import SYS_ROLE_MST_SEED

# revision identifiers, used by Alembic.
revision: str = "c4e7f2a91b06"
down_revision: Union[str, None] = "b1c4d8e29a3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "SYS_USER_MST",
        sa.Column("PWD_CHG_YN", sa.Boolean, nullable=False, server_default=sa.true()),
    )

    # NOT NULL 제약을 걸기 전, 이미 존재할 수 있는 NULL 값을 사번 기반 placeholder로 채운다
    # (§9 리스크 "EMAIL_ADDR 미입력 기존 사원" — 운영팀이 실제 이메일로 재확인·수정 필요).
    op.execute(
        """
        UPDATE "HR_EMPL_MST" SET "EMAIL_ADDR" = "EMPL_NO" || '@placeholder.blueward.co.kr'
        WHERE "EMAIL_ADDR" IS NULL
        """
    )
    op.alter_column("HR_EMPL_MST", "EMAIL_ADDR", nullable=False)

    sys_role_mst = sa.table(
        "SYS_ROLE_MST",
        sa.column("ROLE_ID", postgresql.UUID(as_uuid=True)),
        sa.column("ROLE_CD", sa.String),
        sa.column("ROLE_NM", sa.String),
        sa.column("ROLE_DESC", sa.Text),
        sa.column("PERM_JSON", postgresql.JSONB),
    )
    employee_role = next(row for row in SYS_ROLE_MST_SEED if row["ROLE_CD"] == "EMPLOYEE")
    op.execute(
        pg_insert(sys_role_mst)
        .values(
            ROLE_ID=uuid.uuid4(),
            ROLE_CD=employee_role["ROLE_CD"],
            ROLE_NM=employee_role["ROLE_NM"],
            ROLE_DESC=employee_role["ROLE_DESC"],
            PERM_JSON=employee_role["PERM_JSON"],
        )
        .on_conflict_do_nothing(index_elements=["ROLE_CD"])
    )


def downgrade() -> None:
    op.execute("""DELETE FROM "SYS_ROLE_MST" WHERE "ROLE_CD" = 'EMPLOYEE'""")
    op.alter_column("HR_EMPL_MST", "EMAIL_ADDR", nullable=True)
    op.drop_column("SYS_USER_MST", "PWD_CHG_YN")
