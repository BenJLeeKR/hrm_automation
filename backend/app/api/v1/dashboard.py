import re
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.repositories import dashboard as dashboard_repo
from app.schemas.dashboard import (
    DashboardSummaryOut,
    DeptUtilizationItem,
    JobTypeDistributionItem,
    UtilizationByTypeOut,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

_MONTH_PATTERN = re.compile(r"^\d{6}$")


@router.get(
    "/summary", response_model=DashboardSummaryOut, dependencies=[Depends(require_permission("dashboard", "view"))]
)
def get_summary(
    as_of: date | None = Query(None, description="기준일 — 생략 시 오늘"),
    db: Session = Depends(get_db),
) -> DashboardSummaryOut:
    """대시보드 KPI 카드 집계 (SCR-002, 로드맵 §8 다음 작업 1번)"""
    return DashboardSummaryOut(**dashboard_repo.get_summary(db, as_of=as_of or date.today()))


@router.get(
    "/dept-utilization",
    response_model=list[DeptUtilizationItem],
    dependencies=[Depends(require_permission("dashboard", "view"))],
)
def get_dept_utilization(
    as_of: date | None = Query(None, description="기준일 — 생략 시 오늘"),
    db: Session = Depends(get_db),
) -> list[DeptUtilizationItem]:
    """부서별 평균 가동률 (SCR-002)"""
    rows = dashboard_repo.get_dept_utilization(db, as_of=as_of or date.today())
    return [DeptUtilizationItem(**row) for row in rows]


@router.get(
    "/job-type-distribution",
    response_model=list[JobTypeDistributionItem],
    dependencies=[Depends(require_permission("dashboard", "view"))],
)
def get_job_type_distribution(db: Session = Depends(get_db)) -> list[JobTypeDistributionItem]:
    """직무 유형별 인력 분포 (SCR-002)"""
    return [JobTypeDistributionItem(**row) for row in dashboard_repo.get_job_type_distribution(db)]


@router.get(
    "/utilization-by-type",
    response_model=UtilizationByTypeOut,
    dependencies=[Depends(require_permission("dashboard", "view"))],
)
def get_utilization_by_type(
    month: str = Query(..., description="기준월 (yyyyMM 형식, 예: 202607)"),
    db: Session = Depends(get_db),
) -> UtilizationByTypeOut:
    """3단계 조직 평균 가동률 (SCR-002, `ASGN_TYPE_CD` RUNNING → +COMMITTED → +PROPOSED)"""
    if not _MONTH_PATTERN.match(month):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="month은 yyyyMM 형식이어야 합니다.")
    year, mon = int(month[:4]), int(month[4:])
    if not 1 <= mon <= 12:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="month의 월 값이 유효하지 않습니다.")
    return UtilizationByTypeOut(**dashboard_repo.get_utilization_by_type(db, year=year, month=mon))
