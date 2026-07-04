import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hr_empl_role_rel import HrEmplRoleRel


def list_employee_roles(db: Session, *, empl_id: uuid.UUID | None = None) -> list[HrEmplRoleRel]:
    """사원역할 연결 목록 조회 — 사원 목록/상세 화면의 "보유 역할" 배지 표시용."""
    stmt = select(HrEmplRoleRel)
    if empl_id is not None:
        stmt = stmt.where(HrEmplRoleRel.EMPL_ID == empl_id)
    return list(db.scalars(stmt))
