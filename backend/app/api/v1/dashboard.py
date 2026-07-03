import re
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.repositories import dashboard as dashboard_repo
from app.schemas.dashboard import (
    DashboardSummaryOut,
    DataQualityOut,
    DeptUtilizationItem,
    EndingAssignmentItem,
    HeadcountTrendItem,
    JobTypeDistributionItem,
    RecentEmployeeItem,
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


@router.get(
    "/data-quality", response_model=DataQualityOut, dependencies=[Depends(require_permission("dashboard", "view"))]
)
def get_data_quality(db: Session = Depends(get_db)) -> DataQualityOut:
    """데이터 품질 점검 요약 (프론트엔드 `/dashboard` "데이터 품질 점검" 위젯 참조)"""
    return DataQualityOut(**dashboard_repo.get_data_quality(db))


@router.get(
    "/ending-this-month",
    response_model=list[EndingAssignmentItem],
    dependencies=[Depends(require_permission("dashboard", "view"))],
)
def get_ending_this_month(
    as_of: date | None = Query(None, description="기준일 — 생략 시 오늘"),
    db: Session = Depends(get_db),
) -> list[EndingAssignmentItem]:
    """이번 달 투입 종료 예정 목록 (프론트엔드 `/dashboard` 위젯 참조)"""
    rows = dashboard_repo.get_ending_this_month(db, as_of=as_of or date.today())
    return [EndingAssignmentItem(**row) for row in rows]


@router.get(
    "/recent-employees",
    response_model=list[RecentEmployeeItem],
    dependencies=[Depends(require_permission("dashboard", "view"))],
)
def get_recent_employees(
    limit: int = Query(10, ge=1, le=50, description="조회할 최근 입사자 수"),
    db: Session = Depends(get_db),
) -> list[RecentEmployeeItem]:
    """최근 입사자 목록 (프론트엔드 `/dashboard` 위젯 참조)"""
    return [RecentEmployeeItem(**row) for row in dashboard_repo.get_recent_employees(db, limit=limit)]


@router.get(
    "/headcount-trend",
    response_model=list[HeadcountTrendItem],
    dependencies=[Depends(require_permission("dashboard", "view"))],
)
def get_headcount_trend(
    months: int = Query(12, ge=1, le=36, description="조회할 개월 수 (당월 포함)"),
    as_of: date | None = Query(None, description="기준일 — 생략 시 오늘"),
    db: Session = Depends(get_db),
) -> list[HeadcountTrendItem]:
    """월별 인력 추이 (프론트엔드 `/dashboard` "월별 인력 추이" 차트 참조)"""
    rows = dashboard_repo.get_headcount_trend(db, as_of=as_of or date.today(), months=months)
    return [HeadcountTrendItem(**row) for row in rows]
