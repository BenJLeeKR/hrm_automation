import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hr_skill_mst import HrSkillMst


def list_skills(
    db: Session,
    *,
    skill_grp_cd: str | None = None,
    use_yn: bool | None = True,
) -> list[HrSkillMst]:
    """기술 목록 조회 — 그룹 코드 필터, 이름 기준 정렬. `use_yn=None`이면 비활성 기술도 포함."""
    stmt = select(HrSkillMst)
    if skill_grp_cd is not None:
        stmt = stmt.where(HrSkillMst.SKILL_GRP_CD == skill_grp_cd)
    if use_yn is not None:
        stmt = stmt.where(HrSkillMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrSkillMst.SKILL_NM)))


def get_skill(db: Session, skill_id: uuid.UUID) -> HrSkillMst | None:
    return db.get(HrSkillMst, skill_id)


def create_skill(db: Session, data: dict) -> HrSkillMst:
    skill = HrSkillMst(**data)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill: HrSkillMst, data: dict) -> HrSkillMst:
    """전달된 필드만 갱신 (부분 업데이트)."""
    for field, value in data.items():
        setattr(skill, field, value)
    db.commit()
    db.refresh(skill)
    return skill
