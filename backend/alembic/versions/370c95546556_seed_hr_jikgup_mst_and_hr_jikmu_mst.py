"""seed HR_JIKGUP_MST (10종) and HR_JIKMU_MST (12종)

Seed 근거: backend/app/db/seed/hr_jikgup_mst_seed.py, hr_jikmu_mst_seed.py
(설계서 §5.3.2/§5.3.3 그대로 확정 — MVP 초안 아님). 이 리비전에서 직접 목록을
재작성하지 않고 해당 모듈을 import해 재사용한다.

`HR_JIKGUP_MST`/`HR_JIKMU_MST` 테이블 자체는 이전 리비전(28ce52377e32)에서 이미
생성·적용되었으므로(실 서버에 이미 존재), 그 리비전을 되돌려 수정하지 않고 새 리비전으로
Seed만 추가한다.

이전 리비전들과 동일하게 로컬 환경에 alembic 패키지가 없어 실 DB 적용 검증은 아직
수행하지 못했다 — 로드맵 [BACKLOG]HRM_Automation_System_Roadmap.md §7 완료 내역 참조.

Revision ID: 370c95546556
Revises: a5754b3eb5f3
Create Date: 2026-07-03

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from app.db.seed.hr_jikgup_mst_seed import HR_JIKGUP_MST_SEED
from app.db.seed.hr_jikmu_mst_seed import HR_JIKMU_MST_SEED

# revision identifiers, used by Alembic.
revision: str = "370c95546556"
down_revision: Union[str, None] = "a5754b3eb5f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    hr_jikgup_mst = sa.table(
        "HR_JIKGUP_MST",
        sa.column("JIKGUP_ID", postgresql.UUID(as_uuid=True)),
        sa.column("JIKGUP_CD", sa.String),
        sa.column("JIKGUP_NM", sa.String),
        sa.column("JIKGUP_ORD", sa.SmallInteger),
    )
    op.bulk_insert(
        hr_jikgup_mst,
        [
            {
                "JIKGUP_ID": uuid.uuid4(),
                "JIKGUP_CD": row["JIKGUP_CD"],
                "JIKGUP_NM": row["JIKGUP_NM"],
                "JIKGUP_ORD": row["JIKGUP_ORD"],
            }
            for row in HR_JIKGUP_MST_SEED
        ],
    )

    hr_jikmu_mst = sa.table(
        "HR_JIKMU_MST",
        sa.column("JIKMU_ID", postgresql.UUID(as_uuid=True)),
        sa.column("JIKMU_CD", sa.String),
        sa.column("JIKMU_NM", sa.String),
        sa.column("JIKMU_GRP_CD", sa.String),
    )
    op.bulk_insert(
        hr_jikmu_mst,
        [
            {
                "JIKMU_ID": uuid.uuid4(),
                "JIKMU_CD": row["JIKMU_CD"],
                "JIKMU_NM": row["JIKMU_NM"],
                "JIKMU_GRP_CD": row["JIKMU_GRP_CD"],
            }
            for row in HR_JIKMU_MST_SEED
        ],
    )


def downgrade() -> None:
    op.execute('DELETE FROM "HR_JIKMU_MST"')
    op.execute('DELETE FROM "HR_JIKGUP_MST"')
