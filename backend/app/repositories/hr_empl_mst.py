import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hr_empl_mst import HrEmplMst


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
