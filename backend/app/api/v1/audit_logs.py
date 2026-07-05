import io
import uuid
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.core.pagination import PaginationParams
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_audit_log import list_audit_logs
from app.schemas.sys_audit_log import AuditLogListResponse

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])

_TGT_TBL_NM = "SYS_AUDIT_LOG"
_EXPORT_HEADERS = ["시각", "사용자", "작업", "대상 테이블", "대상 ID", "IP"]
_ACT_CD_LABELS = {"CREATE": "생성", "UPDATE": "수정", "DELETE": "삭제", "LOGIN": "로그인", "IMPORT": "일괄등록", "EXPORT": "내보내기"}
# 목록 화면은 skip/limit(최대 200)으로 페이지네이션하지만, Excel 내보내기는 현재 필터
# 조건에 해당하는 전체 행을 담아야 한다 — `list_employees_for_export`와 동일한 원칙으로
# 사실상 무제한에 가까운 limit 하나로 호출한다(감사 로그가 이 한도를 넘길 정도로 쌓이면
# 별도 페이지네이션 내보내기 방식으로 재검토 필요).
_EXPORT_MAX_ROWS = 100_000


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
    """감사 로그 목록 조회 (로드맵 §8 "설정 화면 구현", SCR-016). Excel 내보내기는
    `GET /audit-logs/export`(§9-1)로 별도 제공한다."""
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


@router.get("/export")
def export_audit_logs(
    request: Request,
    user_lgid: str | None = Query(None, description="수행 사용자 로그인 ID 검색 (부분 일치)"),
    act_cd: str | None = Query(None, description="행위 코드 (CREATE/UPDATE/DELETE/LOGIN/IMPORT/EXPORT 등)"),
    tgt_tbl_nm: str | None = Query(None, description="대상 테이블명 (예: HR_EMPL_MST)"),
    date_from: datetime | None = Query(None, description="조회 시작 일시"),
    date_to: datetime | None = Query(None, description="조회 종료 일시"),
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("settings_audit_logs", "excel")),
) -> StreamingResponse:
    """감사 로그 Excel 내보내기 (SCR-016 "Excel 내보내기" 버튼, §9-1) — 화면 조회와 동일한
    필터(사용자/행위/대상테이블/기간)로 전체 행을 xlsx로 내보낸다(사원 목록 Excel
    내보내기와 동일한 `openpyxl` 사용 패턴). `tgt_id` 단건 필터는 사원 상세 화면의
    "변경 이력" 탭 전용이라 이번 내보내기 대상(설정 화면 전체 로그)에서는 제외한다.
    """
    items, _ = list_audit_logs(
        db,
        skip=0,
        limit=_EXPORT_MAX_ROWS,
        user_lgid=user_lgid,
        act_cd=act_cd,
        tgt_tbl_nm=tgt_tbl_nm,
        date_from=date_from,
        date_to=date_to,
    )

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "감사_로그"
    sheet.append(_EXPORT_HEADERS)
    for item in items:
        sheet.append(
            [
                item["REG_DTTM"].isoformat(),
                item["USER_LGID"],
                _ACT_CD_LABELS.get(item["ACT_CD"], item["ACT_CD"]),
                item["TGT_TBL_NM"],
                str(item["TGT_ID"]) if item["TGT_ID"] else None,
                item["CLNT_IP"],
            ]
        )

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    record_audit(
        db,
        request,
        current_user,
        act_cd="EXPORT",
        tgt_tbl_nm=_TGT_TBL_NM,
        aft_val_json={"row_count": len(items)},
    )

    filename = f"audit_logs_{date.today().isoformat()}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
