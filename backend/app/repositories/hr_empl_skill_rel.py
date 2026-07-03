import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hr_empl_skill_rel import HrEmplSkillRel


def list_employee_skills(
    db: Session,
    *,
    empl_id: uuid.UUID | None = None,
    skill_id: uuid.UUID | None = None,
) -> list[HrEmplSkillRel]:
    """사원기술 연결 목록 조회 — 사원/기술 ID 필터."""
    stmt = select(HrEmplSkillRel)
    if empl_id is not None:
        stmt = stmt.where(HrEmplSkillRel.EMPL_ID == empl_id)
    if skill_id is not None:
        stmt = stmt.where(HrEmplSkillRel.SKILL_ID == skill_id)
    return list(db.scalars(stmt))


def get_employee_skill(db: Session, empl_skill_id: uuid.UUID) -> HrEmplSkillRel | None:
    return db.get(HrEmplSkillRel, empl_skill_id)


def create_employee_skill(db: Session, data: dict) -> HrEmplSkillRel:
    """사원기술 연결 등록. `EMPL_ID`/`SKILL_ID` FK 위반은 호출부(API 라우터)에서
    `sqlalchemy.exc.IntegrityError`를 잡아 처리한다."""
    employee_skill = HrEmplSkillRel(**data)
    db.add(employee_skill)
    db.commit()
    db.refresh(employee_skill)
    return employee_skill


def update_employee_skill(db: Session, employee_skill: HrEmplSkillRel, data: dict) -> HrEmplSkillRel:
    """전달된 필드만 갱신 (부분 업데이트)."""
    for field, value in data.items():
        setattr(employee_skill, field, value)
    db.commit()
    db.refresh(employee_skill)
    return employee_skill
