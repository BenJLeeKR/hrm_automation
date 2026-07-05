from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sys_role_mst import SysRoleMst


def list_roles(db: Session) -> list[SysRoleMst]:
    """역할 목록 조회 — 사용자 관리 화면(SCR-015)의 "역할" 선택 드롭다운 용도."""
    return list(db.scalars(select(SysRoleMst).order_by(SysRoleMst.ROLE_CD)))


def get_role_by_code(db: Session, role_cd: str) -> SysRoleMst | None:
    """역할 코드로 단건 조회 — 사원 계정 자동 생성 시 기본 역할(`EMPLOYEE`) 조회 용도
    (설계서 §5.5 "사원 계정 자동 생성")."""
    return db.scalar(select(SysRoleMst).where(SysRoleMst.ROLE_CD == role_cd))
