import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sys_user_mst import SysUserMst


def get_user_by_login_id(db: Session, user_lgid: str) -> SysUserMst | None:
    return db.scalar(select(SysUserMst).where(SysUserMst.USER_LGID == user_lgid))


def get_user(db: Session, user_id: uuid.UUID) -> SysUserMst | None:
    return db.get(SysUserMst, user_id)


def update_last_login(db: Session, user: SysUserMst) -> SysUserMst:
    user.LAST_LGN_DTTM = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user


def list_users(
    db: Session, *, role_id: uuid.UUID | None = None, use_yn: bool | None = None
) -> list[SysUserMst]:
    """시스템 사용자 목록 조회 (SCR-015 "사용자 관리")."""
    stmt = select(SysUserMst)
    if role_id is not None:
        stmt = stmt.where(SysUserMst.ROLE_ID == role_id)
    if use_yn is not None:
        stmt = stmt.where(SysUserMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(SysUserMst.USER_LGID)))


def create_user(db: Session, data: dict) -> SysUserMst:
    """시스템 사용자 등록. `USER_LGID`/`EMAIL_ADDR` UNIQUE 위반, `ROLE_ID`/`EMPL_ID` FK
    위반은 호출부(API 라우터)에서 `sqlalchemy.exc.IntegrityError`를 잡아 처리한다."""
    user = SysUserMst(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
