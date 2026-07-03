"""add `codes` 화면 권한 키 to SYS_ROLE_MST.PERM_JSON

배경: 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §9 리스크
"departments/positions/job-types 화면 권한 키 미정" — 운영팀 확인 결과(2026-07-03),
부서(`departments`)/직급(`positions`)은 MVP에서 독립 화면으로 보지 않고 "공통 코드/
기준정보"로 취급하기로 확정. 별도 화면 키를 만들지 않고 `codes` 키 하나로 통합하며,
`codes.view`는 전 역할 허용, `codes.create`/`update`/`delete`는 ADMIN/HR_MGR만 허용.

`SYS_ROLE_MST`는 이전 리비전(83fc676b952e)에서 이미 생성·Seed 적용된 상태이므로 그
리비전을 되돌려 수정하지 않고, 기존 행의 `PERM_JSON`을 `jsonb_set`으로 갱신하는 새
리비전을 추가한다. 최신 Seed 소스(`app/db/seed/sys_role_mst_seed.py`)도 동일 내용으로
갱신되어 있어, 이 리비전은 이미 적용된 실 DB 데이터를 그 기준에 맞춰 정정하는 역할이다.

Revision ID: 9c1f3a5d2b7e
Revises: 370c95546556
Create Date: 2026-07-03

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c1f3a5d2b7e"
down_revision: Union[str, None] = "370c95546556"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ROLE_CD -> codes 권한 (view/create/update/delete/excel/admin)
_ADMIN_HR_MGR_CODES_PERM = '{"view": true, "create": true, "update": true, "delete": true, "excel": false, "admin": false}'
_VIEW_ONLY_CODES_PERM = '{"view": true, "create": false, "update": false, "delete": false, "excel": false, "admin": false}'

_FULL_ACCESS_ROLES = ("ADMIN", "HR_MGR")
_VIEW_ONLY_ROLES = ("PM", "TEAM_LEAD", "EXEC", "VIEWER")


def upgrade() -> None:
    for role_cd in _FULL_ACCESS_ROLES:
        op.execute(
            f"""
            UPDATE "SYS_ROLE_MST"
            SET "PERM_JSON" = jsonb_set("PERM_JSON", '{{screens,codes}}', '{_ADMIN_HR_MGR_CODES_PERM}'::jsonb, true)
            WHERE "ROLE_CD" = '{role_cd}'
            """
        )
    for role_cd in _VIEW_ONLY_ROLES:
        op.execute(
            f"""
            UPDATE "SYS_ROLE_MST"
            SET "PERM_JSON" = jsonb_set("PERM_JSON", '{{screens,codes}}', '{_VIEW_ONLY_CODES_PERM}'::jsonb, true)
            WHERE "ROLE_CD" = '{role_cd}'
            """
        )


def downgrade() -> None:
    op.execute("""UPDATE "SYS_ROLE_MST" SET "PERM_JSON" = "PERM_JSON" #- '{screens,codes}'""")
