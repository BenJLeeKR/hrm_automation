import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_role_rel import HrEmplRoleRel
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.hr_jikgup_mst import HrJikgupMst
from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.hr_skill_mst import HrSkillMst


def list_employees(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    dept_id: uuid.UUID | None = None,
    jikmu_id: uuid.UUID | None = None,
    empl_stat_cd: str | None = None,
) -> tuple[list[HrEmplMst], int]:
    """사원 목록 조회 — 부서/직무 유형/재직상태 필터, skip/limit 페이지네이션.

    화면 설계서(SCR-003 사원 목록)의 직무 유형 필터 요건에 대응해 `jikmu_id` 필터를 지원한다.
    """
    stmt = select(HrEmplMst)
    count_stmt = select(func.count()).select_from(HrEmplMst)

    if dept_id is not None:
        stmt = stmt.where(HrEmplMst.DEPT_ID == dept_id)
        count_stmt = count_stmt.where(HrEmplMst.DEPT_ID == dept_id)
    if jikmu_id is not None:
        stmt = stmt.where(HrEmplMst.JIKMU_ID == jikmu_id)
        count_stmt = count_stmt.where(HrEmplMst.JIKMU_ID == jikmu_id)
    if empl_stat_cd is not None:
        stmt = stmt.where(HrEmplMst.EMPL_STAT_CD == empl_stat_cd)
        count_stmt = count_stmt.where(HrEmplMst.EMPL_STAT_CD == empl_stat_cd)

    total = db.scalar(count_stmt) or 0
    items = list(db.scalars(stmt.order_by(HrEmplMst.EMPL_NO).offset(skip).limit(limit)))
    return items, total


def get_employee(db: Session, empl_id: uuid.UUID) -> HrEmplMst | None:
    return db.get(HrEmplMst, empl_id)


def create_employee(db: Session, data: dict) -> HrEmplMst:
    """사원 등록. `EMPL_NO`/`EMAIL_ADDR` UNIQUE 위반, `DEPT_ID`/`JIKGUP_ID`/`JIKMU_ID` FK 위반은
    호출부(API 라우터)에서 `sqlalchemy.exc.IntegrityError`를 잡아 처리한다."""
    employee = HrEmplMst(**data)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee: HrEmplMst, data: dict) -> HrEmplMst:
    """전달된 필드만 갱신 (부분 업데이트)."""
    for field, value in data.items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def retire_employee(db: Session, employee: HrEmplMst, retir_dt: date | None = None) -> HrEmplMst:
    """퇴직 처리 — 로우 삭제가 아니라 `EMPL_STAT_CD='RETIRED'`로 전환하는 소프트 삭제.
    `RETIR_DT` 미지정 시 오늘 날짜로 기록한다 (로드맵 §8 다음 작업 1번)."""
    employee.EMPL_STAT_CD = "RETIRED"
    employee.RETIR_DT = retir_dt or date.today()
    db.commit()
    db.refresh(employee)
    return employee


def list_employees_for_export(
    db: Session,
    *,
    dept_id: uuid.UUID | None = None,
    jikmu_id: uuid.UUID | None = None,
    empl_stat_cd: str | None = None,
) -> list[dict]:
    """Excel Export용 사원 목록 조회 (`[DESIGN]HRM_Screen_Design.md` SCR-003 "인력마스터_ResourceTable"
    시트 컬럼 매핑 기준). `list_employees`와 동일한 필터를 지원하되, 화면 미리보기용 페이지네이션
    없이 필터에 해당하는 전체 행을 반환한다(설계서: "현재 필터 결과를 ... Export").

    보유역할(`HR_EMPL_ROLE_REL`)·주요기술(`HR_EMPL_SKILL_REL`)은 N:M 관계라 사원별로
    쉼표로 이어붙여 반환한다. 숙련도는 원본 Excel 서식 자체가 "전체 기술에 동일 숙련도"
    한 칸만 두는 손실 매핑이라(설계서 §"Excel Import/Export 컬럼 매핑" 참조), 여러 기술의
    숙련도가 다르면 그중 최댓값을 대표값으로 내보낸다.
    """
    stmt = (
        select(HrEmplMst, HrDeptMst.DEPT_NM, HrJikgupMst.JIKGUP_NM)
        .outerjoin(HrDeptMst, HrDeptMst.DEPT_ID == HrEmplMst.DEPT_ID)
        .outerjoin(HrJikgupMst, HrJikgupMst.JIKGUP_ID == HrEmplMst.JIKGUP_ID)
    )
    if dept_id is not None:
        stmt = stmt.where(HrEmplMst.DEPT_ID == dept_id)
    if jikmu_id is not None:
        stmt = stmt.where(HrEmplMst.JIKMU_ID == jikmu_id)
    if empl_stat_cd is not None:
        stmt = stmt.where(HrEmplMst.EMPL_STAT_CD == empl_stat_cd)
    rows = db.execute(stmt.order_by(HrEmplMst.EMPL_NO)).all()

    empl_ids = [row.HrEmplMst.EMPL_ID for row in rows]
    roles_by_empl = _aggregate_roles(db, empl_ids)
    skills_by_empl = _aggregate_skills(db, empl_ids)

    return [
        {
            "employee": row.HrEmplMst,
            "DEPT_NM": row.DEPT_NM,
            "JIKGUP_NM": row.JIKGUP_NM,
            "ROLES": roles_by_empl.get(row.HrEmplMst.EMPL_ID, ""),
            "SKILLS": skills_by_empl.get(row.HrEmplMst.EMPL_ID, ("", None))[0],
            "PRFCY_LEVL": skills_by_empl.get(row.HrEmplMst.EMPL_ID, ("", None))[1],
        }
        for row in rows
    ]


def _aggregate_roles(db: Session, empl_ids: list[uuid.UUID]) -> dict[uuid.UUID, str]:
    if not empl_ids:
        return {}
    stmt = (
        select(HrEmplRoleRel.EMPL_ID, func.string_agg(HrJikmuMst.JIKMU_CD, ", "))
        .join(HrJikmuMst, HrJikmuMst.JIKMU_ID == HrEmplRoleRel.JIKMU_ID)
        .where(HrEmplRoleRel.EMPL_ID.in_(empl_ids))
        .group_by(HrEmplRoleRel.EMPL_ID)
    )
    return dict(db.execute(stmt).all())


def _aggregate_skills(db: Session, empl_ids: list[uuid.UUID]) -> dict[uuid.UUID, tuple[str, int | None]]:
    if not empl_ids:
        return {}
    stmt = (
        select(
            HrEmplSkillRel.EMPL_ID,
            func.string_agg(HrSkillMst.SKILL_NM, ", "),
            func.max(HrEmplSkillRel.PRFCY_LEVL),
        )
        .join(HrSkillMst, HrSkillMst.SKILL_ID == HrEmplSkillRel.SKILL_ID)
        .where(HrEmplSkillRel.EMPL_ID.in_(empl_ids))
        .group_by(HrEmplSkillRel.EMPL_ID)
    )
    return {row[0]: (row[1], row[2]) for row in db.execute(stmt).all()}
