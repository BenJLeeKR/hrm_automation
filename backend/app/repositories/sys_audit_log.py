from sqlalchemy.orm import Session

from app.models.sys_audit_log import SysAuditLog


def create_audit_log(db: Session, data: dict) -> SysAuditLog:
    """감사 로그 기록 (append-only) — 등록/수정/로그인 등 행위 발생 시점에 호출한다."""
    log = SysAuditLog(**data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
