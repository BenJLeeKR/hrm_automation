import uuid
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.sys_audit_log import SysAuditLog
from app.models.sys_user_mst import SysUserMst


def create_audit_log(db: Session, data: dict) -> SysAuditLog:
    """감사 로그 기록 (append-only) — 등록/수정/로그인 등 행위 발생 시점에 호출한다."""
    log = SysAuditLog(**data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_audit_logs(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    user_lgid: str | None = None,
    act_cd: str | None = None,
    tgt_tbl_nm: str | None = None,
    tgt_id: uuid.UUID | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> tuple[list[dict], int]:
    """감사 로그 목록 조회 (SCR-016 "감사 로그") — 수행 사용자 로그인 ID를 조인해 함께 반환한다.

    `tgt_id`는 사원 상세 화면(SCR-004) "변경 이력" 탭처럼 특정 대상 1건의 변경 이력만
    조회할 때 사용한다(§9-1 참조) — `tgt_tbl_nm`과 함께 지정해야 다른 테이블의 동일 UUID
    충돌을 피할 수 있으나, 화면 호출부가 항상 둘 다 넘기므로 이 함수는 강제하지 않는다.
    """
    stmt = select(SysAuditLog, SysUserMst.USER_LGID).join(SysUserMst, SysUserMst.USER_ID == SysAuditLog.USER_ID)
    count_stmt = select(func.count()).select_from(SysAuditLog).join(SysUserMst, SysUserMst.USER_ID == SysAuditLog.USER_ID)

    if user_lgid is not None:
        stmt = stmt.where(SysUserMst.USER_LGID.ilike(f"%{user_lgid}%"))
        count_stmt = count_stmt.where(SysUserMst.USER_LGID.ilike(f"%{user_lgid}%"))
    if act_cd is not None:
        stmt = stmt.where(SysAuditLog.ACT_CD == act_cd)
        count_stmt = count_stmt.where(SysAuditLog.ACT_CD == act_cd)
    if tgt_tbl_nm is not None:
        stmt = stmt.where(SysAuditLog.TGT_TBL_NM == tgt_tbl_nm)
        count_stmt = count_stmt.where(SysAuditLog.TGT_TBL_NM == tgt_tbl_nm)
    if tgt_id is not None:
        stmt = stmt.where(SysAuditLog.TGT_ID == tgt_id)
        count_stmt = count_stmt.where(SysAuditLog.TGT_ID == tgt_id)
    if date_from is not None:
        stmt = stmt.where(SysAuditLog.REG_DTTM >= date_from)
        count_stmt = count_stmt.where(SysAuditLog.REG_DTTM >= date_from)
    if date_to is not None:
        stmt = stmt.where(SysAuditLog.REG_DTTM <= date_to)
        count_stmt = count_stmt.where(SysAuditLog.REG_DTTM <= date_to)

    total = db.scalar(count_stmt) or 0
    rows = db.execute(stmt.order_by(SysAuditLog.REG_DTTM.desc()).offset(skip).limit(limit)).all()
    items = [
        {
            "AUDIT_ID": log.AUDIT_ID,
            "USER_ID": log.USER_ID,
            "USER_LGID": user_lgid_val,
            "ACT_CD": log.ACT_CD,
            "TGT_TBL_NM": log.TGT_TBL_NM,
            "TGT_ID": log.TGT_ID,
            "BFR_VAL_JSON": log.BFR_VAL_JSON,
            "AFT_VAL_JSON": log.AFT_VAL_JSON,
            "CLNT_IP": log.CLNT_IP,
            "USER_AGT": log.USER_AGT,
            "REG_DTTM": log.REG_DTTM,
        }
        for log, user_lgid_val in rows
    ]
    return items, total
