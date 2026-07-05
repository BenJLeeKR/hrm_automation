"""사원-계정 연동 설계 반영 1-4: HR_MGR의 settings_users.update 권한 확대

배경: 로드맵 §8 다음 작업 1번의 1-4 (`[DESIGN]HRM_Automation_System_Design_v0_6.md`
§5.5 "직원 역할(업무 권한) 배정"). `HR_MGR`이 `EMPL_ID`가 연결된(사원과 연동된) 계정의
업무 역할(PM/TEAM_LEAD/EXEC/EMPLOYEE/VIEWER)만 변경할 수 있도록 `settings_users.update`
권한을 확대한다 — `view`/`create`/`delete`는 이번 범위에서 다루지 않아 그대로 유지한다.
"`EMPL_ID` 연결 계정만"·"업무 역할만"이라는 값(role)·행(row) 단위 제약은 `PERM_JSON`
(화면/버튼 단위)으로 표현할 수 없어 `app/api/v1/users.py`의 `patch_user`에서 API 레이어
검증을 별도로 추가한다(`PERMISSION_MATRIX.md` §5-7 참조).

`SYS_ROLE_MST`는 이전 리비전(83fc676b952e)에서 이미 생성·Seed 적용된 상태이므로 그
리비전을 되돌려 수정하지 않고, `9c1f3a5d2b7e`(codes 권한 추가)와 동일한 패턴으로
`jsonb_set`을 사용해 `HR_MGR` 행의 `PERM_JSON`만 갱신한다.

Revision ID: e8a2f5c7b91d
Revises: c4e7f2a91b06
Create Date: 2026-07-06

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e8a2f5c7b91d"
down_revision: Union[str, None] = "c4e7f2a91b06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_HR_MGR_SETTINGS_USERS_PERM = (
    '{"view": false, "create": false, "update": true, "delete": false, "excel": false, "admin": false}'
)
_ORIGINAL_HR_MGR_SETTINGS_USERS_PERM = (
    '{"view": false, "create": false, "update": false, "delete": false, "excel": false, "admin": false}'
)


def upgrade() -> None:
    op.execute(
        f"""
        UPDATE "SYS_ROLE_MST"
        SET "PERM_JSON" = jsonb_set("PERM_JSON", '{{screens,settings_users}}', '{_HR_MGR_SETTINGS_USERS_PERM}'::jsonb, true)
        WHERE "ROLE_CD" = 'HR_MGR'
        """
    )


def downgrade() -> None:
    op.execute(
        f"""
        UPDATE "SYS_ROLE_MST"
        SET "PERM_JSON" = jsonb_set("PERM_JSON", '{{screens,settings_users}}', '{_ORIGINAL_HR_MGR_SETTINGS_USERS_PERM}'::jsonb, true)
        WHERE "ROLE_CD" = 'HR_MGR'
        """
    )
