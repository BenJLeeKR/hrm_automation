import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.repositories.reports import build_report, build_utilization_matrix
from app.schemas.reports import ReportOut, ReportSendRequest, ReportSendResponse, UtilizationMatrixOut
from app.services.teams_notify import TeamsNotifyError, send_teams_message

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get(
    "/weekly", response_model=ReportOut, dependencies=[Depends(require_permission("reports", "view"))]
)
def get_weekly_report(
    week: str | None = Query(None, description="ISO 주차 (예: 2026-W27) — 생략 시 이번 주"),
    db: Session = Depends(get_db),
) -> ReportOut:
    """주간 리포트 (SCR-013 탭 1, 로드맵 §8 "리포트 화면 구현").

    설계서상 "주간 리포트"와 "월간 리포트"는 기간 단위만 다를 뿐 동일한 구조라
    `build_report`(기준일 하나만 받는 즉시 계산)를 공유한다 — 특정 주차/월의 과거
    스냅샷을 보관하지 않으므로, 지정한 날짜가 속한 시점 기준으로 현재 데이터를
    재계산한 결과를 반환한다(`HR_AVAIL_SNAP` 배치 미구현과 동일한 제약, §9 참조).
    """
    as_of = _parse_iso_week(week) if week else date.today()
    return ReportOut(**build_report(db, as_of=as_of))


@router.get(
    "/monthly", response_model=ReportOut, dependencies=[Depends(require_permission("reports", "view"))]
)
def get_monthly_report(
    month: str | None = Query(None, description="YYYYMM — 생략 시 이번 달"),
    db: Session = Depends(get_db),
) -> ReportOut:
    """월간 리포트 (SCR-013 탭 2) — `get_weekly_report`와 동일한 집계를 월 단위로 제공한다."""
    as_of = _parse_yyyymm(month) if month else date.today()
    return ReportOut(**build_report(db, as_of=as_of))


@router.post(
    "/send", response_model=ReportSendResponse, dependencies=[Depends(require_permission("reports", "admin"))]
)
def send_report(payload: ReportSendRequest, db: Session = Depends(get_db)) -> ReportSendResponse:
    """리포트 수동 발송 (SCR-013 "리포트 발송" 버튼, §9-1) — 화면에서 조회 중인 주간/월간
    리포트 요약을 Teams Incoming Webhook으로 전송한다. 리포트 조회와 동일한
    `build_report`를 재사용해 새 집계 로직을 만들지 않는다. `TEAMS_WEBHOOK_URL` 미설정
    시에는 `PJT_ASGN_END_ALERT` 배치와 동일하게 예외 없이 `sent=False`로 안내한다.
    """
    if payload.report_type == "weekly":
        as_of = _parse_iso_week(payload.period) if payload.period else date.today()
        iso_year, iso_week, _ = as_of.isocalendar()
        label = f"주간 리포트 ({iso_year}-W{iso_week:02d})"
    else:
        as_of = _parse_yyyymm(payload.period) if payload.period else date.today()
        label = f"월간 리포트 ({as_of.strftime('%Y-%m')})"

    report = build_report(db, as_of=as_of)
    text = (
        f"[HRM 자동화 시스템] {label}\n"
        f"재직 인원: {report['total_active_employees']}명\n"
        f"즉시 가동: {report['available_count']}명 · 부분 가동: {report['partial_count']}명 · "
        f"풀 투입: {report['full_count']}명\n"
        f"종료 예정: {report['ending_count']}건 · 직무 미등록: {report['job_missing_count']}명"
    )

    try:
        sent = send_teams_message(text)
    except TeamsNotifyError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from None

    message = "Teams로 리포트를 전송했습니다." if sent else "TEAMS_WEBHOOK_URL이 설정되어 있지 않아 전송을 건너뛰었습니다."
    return ReportSendResponse(sent=sent, message=message)


def _parse_iso_week(week: str) -> date:
    try:
        year_str, week_str = week.split("-W")
        return date.fromisocalendar(int(year_str), int(week_str), 1)
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="week는 'YYYY-Www' 형식이어야 합니다 (예: 2026-W27)."
        ) from None


@router.get(
    "/utilization-matrix",
    response_model=UtilizationMatrixOut,
    dependencies=[Depends(require_permission("reports", "view"))],
)
def get_utilization_matrix(
    from_: str = Query(..., alias="from", description="시작월 YYYYMM"),
    to: str = Query(..., description="종료월 YYYYMM"),
    dept_id: uuid.UUID | None = Query(None, description="부서 ID로 필터링 (HR_DEPT_MST.DEPT_ID)"),
    db: Session = Depends(get_db),
) -> UtilizationMatrixOut:
    """월별 가동률 통계 매트릭스 (SCR-013 탭 3, `ResourceManagement_v2.xlsx` "가동률_통계"
    시트 구조) — 인원×프로젝트별 월간 투입률·소계·연평균·조직 평균 3단계를 반환한다.
    """
    from_dt = _parse_yyyymm(from_)
    to_dt = _parse_yyyymm(to)
    if to_dt < from_dt:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="to는 from보다 앞설 수 없습니다.")
    return UtilizationMatrixOut(**build_utilization_matrix(db, from_dt=from_dt, to_dt=to_dt, dept_id=dept_id))


def _parse_yyyymm(month: str) -> date:
    if len(month) != 6 or not month.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="month는 'YYYYMM' 형식이어야 합니다 (예: 202607)."
        )
    return date(int(month[:4]), int(month[4:6]), 1)
