import uuid
from datetime import date

from pydantic import BaseModel


class DashboardSummaryOut(BaseModel):
    """대시보드 KPI 카드 응답 스키마 (`GET /api/v1/dashboard/summary`, SCR-002)."""

    total_active_employees: int
    available_count: int
    partial_count: int
    full_count: int
    ending_this_month_count: int
    avg_utilization_rate: float | None


class DeptUtilizationItem(BaseModel):
    """부서별 평균 가동률 응답 항목 (`GET /api/v1/dashboard/dept-utilization`, SCR-002)."""

    DEPT_ID: uuid.UUID
    DEPT_NM: str
    employee_count: int
    avg_utilization_rate: float


class JobTypeDistributionItem(BaseModel):
    """직무 유형별 인력 분포 응답 항목 (`GET /api/v1/dashboard/job-type-distribution`, SCR-002)."""

    JIKMU_ID: uuid.UUID | None
    JIKMU_NM: str
    employee_count: int


class UtilizationByTypeOut(BaseModel):
    """3단계 조직 평균 가동률 응답 스키마 (`GET /api/v1/dashboard/utilization-by-type`, SCR-002)."""

    month: str
    running_rate: float
    running_committed_rate: float
    all_rate: float


class DataQualityOut(BaseModel):
    """데이터 품질 점검 응답 스키마 (`GET /api/v1/dashboard/data-quality`) — 프론트엔드 `/dashboard`
    "데이터 품질 점검" 위젯(`lib/mock-data.ts`의 `dataQuality`) 참조."""

    skill_missing_count: int
    job_missing_count: int
    over_allocation_count: int


class EndingAssignmentItem(BaseModel):
    """이번 달 투입 종료 예정 응답 항목 (`GET /api/v1/dashboard/ending-this-month`) — 프론트엔드
    `/dashboard` "이달 투입 종료 예정" 위젯(`lib/mock-data.ts`의 `endingThisMonth`) 참조."""

    EMPL_NM: str
    DEPT_NM: str | None
    PJT_NM: str
    ASGN_END_DT: date
    ALLOC_RT: int


class RecentEmployeeItem(BaseModel):
    """최근 입사자 응답 항목 (`GET /api/v1/dashboard/recent-employees`) — 프론트엔드 `/dashboard`
    "최근 입사자" 위젯(`lib/mock-data.ts`의 `recentEmployees`) 참조."""

    EMPL_NO: str
    EMPL_NM: str
    DEPT_NM: str | None
    HIRE_DT: date
    JIKMU_NM: str | None


class HeadcountTrendItem(BaseModel):
    """월별 인력 추이 응답 항목 (`GET /api/v1/dashboard/headcount-trend`) — 프론트엔드 `/dashboard`
    "월별 인력 추이" 차트(`lib/mock-data.ts`의 `headcountTrend`) 참조."""

    month: str
    total: int
    hires: int
    exits: int
