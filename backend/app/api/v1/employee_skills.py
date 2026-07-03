import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.hr_empl_skill_rel import (
    create_employee_skill,
    get_employee_skill,
    list_employee_skills,
    update_employee_skill,
)
from app.schemas.hr_empl_skill_rel import EmployeeSkillCreate, EmployeeSkillOut, EmployeeSkillUpdate

router = APIRouter(prefix="/employee-skills", tags=["employee-skills"])


@router.get("", response_model=list[EmployeeSkillOut])
def get_employee_skills(
    empl_id: uuid.UUID | None = Query(None, description="사원 ID로 필터링 (HR_EMPL_MST.EMPL_ID)"),
    skill_id: uuid.UUID | None = Query(None, description="기술 ID로 필터링 (HR_SKILL_MST.SKILL_ID)"),
    db: Session = Depends(get_db),
) -> list[EmployeeSkillOut]:
    """사원기술 연결 목록 조회 (로드맵 §8 다음 작업 1번)"""
    return list_employee_skills(db, empl_id=empl_id, skill_id=skill_id)


@router.post("", response_model=EmployeeSkillOut, status_code=status.HTTP_201_CREATED)
def post_employee_skill(payload: EmployeeSkillCreate, db: Session = Depends(get_db)) -> EmployeeSkillOut:
    """사원기술 연결 등록"""
    try:
        employee_skill = create_employee_skill(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 사원-기술 조합이거나 사원/기술 ID가 유효하지 않습니다.",
        ) from None
    return employee_skill


@router.patch("/{empl_skill_id}", response_model=EmployeeSkillOut)
def patch_employee_skill(
    empl_skill_id: uuid.UUID, payload: EmployeeSkillUpdate, db: Session = Depends(get_db)
) -> EmployeeSkillOut:
    """사원기술 연결 수정 — 전달된 필드만 갱신"""
    employee_skill = get_employee_skill(db, empl_skill_id)
    if employee_skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원기술 연결 정보를 찾을 수 없습니다.")

    try:
        employee_skill = update_employee_skill(db, employee_skill, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 사원-기술 조합이거나 사원/기술 ID가 유효하지 않습니다.",
        ) from None
    return employee_skill
