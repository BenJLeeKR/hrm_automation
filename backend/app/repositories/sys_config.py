from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sys_config import SysConfig

_NOTIFICATION_GRP = "NOTIFICATION"


def get_config(db: Session, config_key: str) -> SysConfig | None:
    return db.get(SysConfig, config_key)


def list_by_group(db: Session, config_grp: str) -> list[SysConfig]:
    stmt = select(SysConfig).where(SysConfig.CONFIG_GRP == config_grp).order_by(SysConfig.CONFIG_KEY)
    return list(db.scalars(stmt))


def list_notification_configs(db: Session) -> list[SysConfig]:
    return list_by_group(db, _NOTIFICATION_GRP)


def upsert_config_value(db: Session, config_key: str, config_val: str | None, *, upd_user: str | None) -> SysConfig:
    """기존 `SYS_CONFIG` 행의 `CONFIG_VAL`만 갱신한다 — `CONFIG_KEY`는 Seed로 이미 생성되어
    있어야 하며(§5.3.17 초기 Seed), 이 함수는 신규 키를 만들지 않는다."""
    config = db.get(SysConfig, config_key)
    if config is None:
        raise ValueError(f"정의되지 않은 CONFIG_KEY: {config_key}")
    config.CONFIG_VAL = config_val
    config.UPD_USER = upd_user
    db.commit()
    db.refresh(config)
    return config
