import uuid
from datetime import date

from pydantic import BaseModel

from app.schemas.dashboard import DeptUtilizationItem


class SkillDistributionItem(BaseModel):
    """기술별 인력 분포 응답 항목 (`GET /api/v1/reports/{weekly,monthly}`, SCR-013 "기술별 인력 분포 Top 10")."""

    SKILL_ID: uuid.UUID
    SKILL_NM: str
    employee_count: int


class ReportOut(BaseModel):
    """주간/월간 리포트 응답 스키마 (SCR-013 탭 1·2 — 두 탭이 동일한 구조를 공유한다).

    1차 구현 범위(로드맵 §8 "리포트 화면 구현")는 요약 KPI·부서별 가동률·기술별 인력
    분포까지만 다룬다 — "월별 가동률 통계" 매트릭스 탭과 리포트 발송/Excel 내보내기는
    후속 작업으로 분리했다(§9 리스크 참조).
    """

    as_of: date
    total_active_employees: int
    available_count: int
    partial_count: int
    full_count: int
    ending_count: int
    job_missing_count: int
    dept_utilization: list[DeptUtilizationItem]
    skill_distribution: list[SkillDistributionItem]


class UtilizationMatrixRow(BaseModel):
    """월별 가동률 통계 — 사원 1명의 프로젝트 1건에 대한 월별 투입률 행."""

    pjt_nm: str
    asgn_type_cd: str
    monthly: list[int]
    avg: float


class UtilizationMatrixEmployee(BaseModel):
    """월별 가동률 통계 — 사원 1명의 프로젝트 행 목록 + 소계/연평균/100% 초과 월."""

    empl_no: str
    empl_nm: str
    dept_nm: str
    rows: list[UtilizationMatrixRow]
    subtotal: list[int]
    annual_avg: float
    over_100_months: list[str]


class UtilizationMatrixOrgAvg(BaseModel):
    """조직 평균 가동률 3단계 (수행중만 / 수행중+투입준비중 / 전체)."""

    running_only: list[float]
    running_committed: list[float]
    all: list[float]


class UtilizationMatrixOut(BaseModel):
    """월별 가동률 통계 매트릭스 응답 (`GET /api/v1/reports/utilization-matrix`, SCR-013 탭 3)."""

    period: list[str]
    employees: list[UtilizationMatrixEmployee]
    org_avg: UtilizationMatrixOrgAvg
