import uuid

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
