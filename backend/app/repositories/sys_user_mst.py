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
