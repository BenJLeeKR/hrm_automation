import uuid
from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_audit_log import create_audit_log


def record_audit(
    db: Session,
    request: Request,
    user: SysUserMst,
    *,
    act_cd: str,
    tgt_tbl_nm: str,
    tgt_id: uuid.UUID | None = None,
    bfr_val_json: dict[str, Any] | None = None,
    aft_val_json: dict[str, Any] | None = None,
) -> None:
    """요청 컨텍스트(클라이언트 IP/User-Agent)를 포함해 `SYS_AUDIT_LOG`에 감사 로그를 기록한다
    (ERD `backend/docs/ERD.md` §3.14).

    `BFR_VAL_JSON`/`AFT_VAL_JSON`에는 비밀번호 등 민감정보가 담기지 않도록, 호출부에서
    각 도메인의 조회(Out) 스키마로 직렬화한 값만 전달해야 한다 — `SysUserOut`이
    `ENCR_PWD`를 응답에서 제외하는 것과 동일한 원칙(설계서 §11).
    """
    create_audit_log(
        db,
        {
            "USER_ID": user.USER_ID,
            "ACT_CD": act_cd,
            "TGT_TBL_NM": tgt_tbl_nm,
            "TGT_ID": tgt_id,
            "BFR_VAL_JSON": bfr_val_json,
            "AFT_VAL_JSON": aft_val_json,
            "CLNT_IP": request.client.host if request.client else None,
            "USER_AGT": request.headers.get("user-agent"),
        },
    )
