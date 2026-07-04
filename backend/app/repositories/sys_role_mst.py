from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sys_role_mst import SysRoleMst


def list_roles(db: Session) -> list[SysRoleMst]:
    """역할 목록 조회 — 사용자 관리 화면(SCR-015)의 "역할" 선택 드롭다운 용도."""
    return list(db.scalars(select(SysRoleMst).order_by(SysRoleMst.ROLE_CD)))
