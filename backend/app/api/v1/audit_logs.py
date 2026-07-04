import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.pagination import PaginationParams
from app.db.session import get_db
from app.repositories.sys_audit_log import list_audit_logs
from app.schemas.sys_audit_log import AuditLogListResponse

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.get(
    "", response_model=AuditLogListResponse, dependencies=[Depends(require_permission("settings_audit_logs", "view"))]
)
def get_audit_logs(
    pagination: PaginationParams = Depends(),
    user_lgid: str | None = Query(None, description="수행 사용자 로그인 ID 검색 (부분 일치)"),
    act_cd: str | None = Query(None, description="행위 코드 (CREATE/UPDATE/DELETE/LOGIN/IMPORT/EXPORT 등)"),
    tgt_tbl_nm: str | None = Query(None, description="대상 테이블명 (예: HR_EMPL_MST)"),
    tgt_id: uuid.UUID | None = Query(None, description="대상 ID 단건 필터 (예: 사원 상세 화면의 변경 이력 탭)"),
    date_from: datetime | None = Query(None, description="조회 시작 일시"),
    date_to: datetime | None = Query(None, description="조회 종료 일시"),
    db: Session = Depends(get_db),
) -> AuditLogListResponse:
    """감사 로그 목록 조회 (로드맵 §8 "설정 화면 구현", SCR-016).

    1차 구현 범위는 목록 조회만 다룬다 — Excel 내보내기(`GET /audit-logs/export`)는
    후속 작업으로 분리했다(§9 리스크 참조).
    """
    items, total = list_audit_logs(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        user_lgid=user_lgid,
        act_cd=act_cd,
        tgt_tbl_nm=tgt_tbl_nm,
        tgt_id=tgt_id,
        date_from=date_from,
        date_to=date_to,
    )
    return AuditLogListResponse(total=total, skip=pagination.skip, limit=pagination.limit, items=items)
