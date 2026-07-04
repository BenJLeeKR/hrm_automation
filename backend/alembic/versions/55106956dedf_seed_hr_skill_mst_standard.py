"""add unique constraint on HR_SKILL_MST(SKILL_GRP_CD, SKILL_NM) and seed standard skills

Seed 근거: backend/app/db/seed/hr_skill_mst_seed.py (사용자 확정 — 13개 그룹, 110건,
MVP 초안 아님). 이 리비전에서 직접 목록을 재작성하지 않고 해당 모듈을 import해 재사용한다.

기존 로드맵 §9 리스크 "HR_SKILL_MST.SKILL_NM에 유니크 제약 없음 — 중복 등록 시 오류
미발생"도 이 리비전에서 함께 해소한다 — (SKILL_GRP_CD, SKILL_NM) 복합 유니크 제약을
추가해 동일 조합의 중복 등록을 DB 레벨에서 막는다. 같은 이유로 Seed 삽입도
`INSERT ... ON CONFLICT DO NOTHING`으로 처리해, 이 리비전을 다시 실행하거나 이미 같은
조합이 존재해도 중복 행이 생기지 않는다.

`HR_SKILL_MST` 테이블 자체는 이전 리비전(28ce52377e32)에서 이미 생성·적용되었으므로,
그 리비전을 되돌려 수정하지 않고 새 리비전으로 제약 추가 + Seed만 반영한다.

Revision ID: 55106956dedf
Revises: 9c1f3a5d2b7e
Create Date: 2026-07-04

"""
import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import insert as pg_insert

from alembic import op
from app.db.seed.hr_skill_mst_seed import HR_SKILL_MST_SEED

# revision identifiers, used by Alembic.
revision: str = "55106956dedf"
down_revision: Union[str, None] = "9c1f3a5d2b7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_CONSTRAINT_NAME = "uq_hr_skill_mst_grp_nm"


def upgrade() -> None:
    op.create_unique_constraint(_CONSTRAINT_NAME, "HR_SKILL_MST", ["SKILL_GRP_CD", "SKILL_NM"])

    hr_skill_mst = sa.table(
        "HR_SKILL_MST",
        sa.column("SKILL_ID", postgresql.UUID(as_uuid=True)),
        sa.column("SKILL_GRP_CD", sa.String),
        sa.column("SKILL_NM", sa.String),
    )
    stmt = pg_insert(hr_skill_mst).values(
        [
            {"SKILL_ID": uuid.uuid4(), "SKILL_GRP_CD": row["SKILL_GRP_CD"], "SKILL_NM": row["SKILL_NM"]}
            for row in HR_SKILL_MST_SEED
        ]
    ).on_conflict_do_nothing(constraint=_CONSTRAINT_NAME)
    op.execute(stmt)


def downgrade() -> None:
    hr_skill_mst = sa.table(
        "HR_SKILL_MST",
        sa.column("SKILL_GRP_CD", sa.String),
        sa.column("SKILL_NM", sa.String),
    )
    for row in HR_SKILL_MST_SEED:
        op.execute(
            hr_skill_mst.delete().where(
                sa.and_(
                    hr_skill_mst.c.SKILL_GRP_CD == row["SKILL_GRP_CD"],
                    hr_skill_mst.c.SKILL_NM == row["SKILL_NM"],
                )
            )
        )
    op.drop_constraint(_CONSTRAINT_NAME, "HR_SKILL_MST", type_="unique")
