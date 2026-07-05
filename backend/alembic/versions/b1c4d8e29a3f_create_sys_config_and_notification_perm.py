"""create SYS_CONFIG table, seed 알림 채널 그룹, add `settings_notification` 화면 권한 키

배경: 로드맵 §9-1/§9 리스크 "일반 설정 탭이 설계서에 없는 화면" — 2026-07-05 운영팀
확인 결과, "일반 설정"(조직 정보/가동률 정책)은 설계 범위에서 최종 제외되었고 "알림
채널"(Teams Webhook/SMTP)만 `.env` 대신 `SYS_CONFIG` DB + 웹 화면으로 관리하기로
확정되었다(`[DESIGN]HRM_Automation_System_Design_v0_7.md` §5.3.17, §5.5,
`[DESIGN]HRM_Screen_Design_v1_2.md` SCR-017).

이 테이블은 코드베이스 유일하게 UUID가 아닌 문자열(`CONFIG_KEY`)을 PK로 쓴다 — 고정된
설정 키를 사람이 읽을 수 있는 값으로 직접 조회/갱신하는 용도라 UUID가 불필요하기
때문이다. `SYS_ROLE_MST`는 83fc676b952e에서 이미 생성·Seed 적용된 상태이므로 그
리비전을 되돌려 수정하지 않고, `9c1f3a5d2b7e`(codes 권한 추가)와 동일한 패턴으로
`jsonb_set`을 사용해 6개 역할 전부에 `settings_notification` 키를 추가한다 — `ADMIN`만
전체 권한, 나머지는 전부 불허(`settings_audit_logs`와 동일한 원칙).

Revision ID: b1c4d8e29a3f
Revises: 55106956dedf
Create Date: 2026-07-05

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert

from alembic import op
from app.db.seed.sys_config_seed import SYS_CONFIG_SEED

# revision identifiers, used by Alembic.
revision: str = "b1c4d8e29a3f"
down_revision: Union[str, None] = "55106956dedf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_ADMIN_NOTIFICATION_PERM = '{"view": true, "create": false, "update": true, "delete": false, "excel": false, "admin": true}'
_NO_ACCESS_NOTIFICATION_PERM = '{"view": false, "create": false, "update": false, "delete": false, "excel": false, "admin": false}'
_NO_ACCESS_ROLES = ("HR_MGR", "PM", "TEAM_LEAD", "EXEC", "VIEWER")


def upgrade() -> None:
    op.create_table(
        "SYS_CONFIG",
        sa.Column("CONFIG_KEY", sa.String(100), primary_key=True),
        sa.Column("CONFIG_GRP", sa.String(50), nullable=False),
        sa.Column("CONFIG_NM", sa.String(200), nullable=False),
        sa.Column("CONFIG_VAL", sa.Text, nullable=True),
        sa.Column("IS_SECRET", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("CONFIG_DESC", sa.Text, nullable=True),
        sa.Column("UPD_DTTM", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("UPD_USER", sa.String(100), nullable=True),
    )

    sys_config = sa.table(
        "SYS_CONFIG",
        sa.column("CONFIG_KEY", sa.String),
        sa.column("CONFIG_GRP", sa.String),
        sa.column("CONFIG_NM", sa.String),
        sa.column("IS_SECRET", sa.Boolean),
        sa.column("CONFIG_DESC", sa.Text),
    )
    op.execute(pg_insert(sys_config).values(SYS_CONFIG_SEED).on_conflict_do_nothing(index_elements=["CONFIG_KEY"]))

    op.execute(
        f"""
        UPDATE "SYS_ROLE_MST"
        SET "PERM_JSON" = jsonb_set("PERM_JSON", '{{screens,settings_notification}}', '{_ADMIN_NOTIFICATION_PERM}'::jsonb, true)
        WHERE "ROLE_CD" = 'ADMIN'
        """
    )
    for role_cd in _NO_ACCESS_ROLES:
        op.execute(
            f"""
            UPDATE "SYS_ROLE_MST"
            SET "PERM_JSON" = jsonb_set("PERM_JSON", '{{screens,settings_notification}}', '{_NO_ACCESS_NOTIFICATION_PERM}'::jsonb, true)
            WHERE "ROLE_CD" = '{role_cd}'
            """
        )


def downgrade() -> None:
    op.execute("""UPDATE "SYS_ROLE_MST" SET "PERM_JSON" = "PERM_JSON" #- '{screens,settings_notification}'""")
    op.drop_table("SYS_CONFIG")
