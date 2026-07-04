from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.hr_skill_mst import HrSkillMst
from app.repositories.dashboard import get_data_quality, get_dept_utilization, get_summary

_TOP_SKILL_LIMIT = 10  # SCR-013 "기술별 인력 분포 Top 10" 기준


def get_skill_distribution_top(db: Session, *, limit: int = _TOP_SKILL_LIMIT) -> list[dict]:
    """보유 인력이 많은 순으로 상위 N개 기술 분포 (SCR-013 "기술별 인력 분포 Top 10")."""
    stmt = (
        select(HrSkillMst.SKILL_ID, HrSkillMst.SKILL_NM, func.count(HrEmplSkillRel.EMPL_ID).label("employee_count"))
        .select_from(HrEmplSkillRel)
        .join(HrSkillMst, HrSkillMst.SKILL_ID == HrEmplSkillRel.SKILL_ID)
        .group_by(HrSkillMst.SKILL_ID, HrSkillMst.SKILL_NM)
        .order_by(func.count(HrEmplSkillRel.EMPL_ID).desc())
        .limit(limit)
    )
    return [
        {"SKILL_ID": row.SKILL_ID, "SKILL_NM": row.SKILL_NM, "employee_count": row.employee_count}
        for row in db.execute(stmt).all()
    ]


def build_report(db: Session, *, as_of: date) -> dict:
    """주간/월간 리포트 공통 데이터 (SCR-013 탭 1·2 — "주간 리포트와 동일 구조, 기간만
    월 단위" 설계에 따라 두 탭이 같은 집계를 공유한다). 대시보드 집계 함수를 그대로
    재사용하고, 리포트 전용 위젯인 "기술별 인력 분포"만 신규로 추가한다."""
    summary = get_summary(db, as_of=as_of)
    return {
        "as_of": as_of,
        "total_active_employees": summary["total_active_employees"],
        "available_count": summary["available_count"],
        "partial_count": summary["partial_count"],
        "full_count": summary["full_count"],
        "ending_count": summary["ending_this_month_count"],
        "job_missing_count": get_data_quality(db)["job_missing_count"],
        "dept_utilization": get_dept_utilization(db, as_of=as_of),
        "skill_distribution": get_skill_distribution_top(db),
    }
