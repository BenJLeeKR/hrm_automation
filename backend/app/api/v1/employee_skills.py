import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.hr_empl_skill_rel import (
    create_employee_skill,
    get_employee_skill,
    list_employee_skills,
    update_employee_skill,
)
from app.schemas.hr_empl_skill_rel import EmployeeSkillCreate, EmployeeSkillOut, EmployeeSkillUpdate

# "skills" 화면 권한을 재사용한다 — PERM_JSON에 사원기술 연결 전용 화면 키가 별도로
# 정의되어 있지 않고(설계서 §5.3.13/PERMISSION_MATRIX.md 기준), 화면 설계서상 사원기술
# 연결 관리는 기술 관리 화면의 일부 기능이라 동일 권한으로 취급한다.
router = APIRouter(prefix="/employee-skills", tags=["employee-skills"])

_TGT_TBL_NM = "HR_EMPL_SKILL_REL"


@router.get("", response_model=list[EmployeeSkillOut], dependencies=[Depends(require_permission("skills", "view"))])
def get_employee_skills(
    empl_id: uuid.UUID | None = Query(None, description="사원 ID로 필터링 (HR_EMPL_MST.EMPL_ID)"),
    skill_id: uuid.UUID | None = Query(None, description="기술 ID로 필터링 (HR_SKILL_MST.SKILL_ID)"),
    db: Session = Depends(get_db),
) -> list[EmployeeSkillOut]:
    """사원기술 연결 목록 조회 (로드맵 §8 다음 작업 1번)"""
    return list_employee_skills(db, empl_id=empl_id, skill_id=skill_id)


@router.post("", response_model=EmployeeSkillOut, status_code=status.HTTP_201_CREATED)
def post_employee_skill(
    payload: EmployeeSkillCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("skills", "create")),
) -> EmployeeSkillOut:
    """사원기술 연결 등록"""
    try:
        employee_skill = create_employee_skill(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 사원-기술 조합이거나 사원/기술 ID가 유효하지 않습니다.",
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee_skill.EMPL_SKILL_ID,
        aft_val_json=EmployeeSkillOut.model_validate(employee_skill).model_dump(mode="json"),
    )
    return employee_skill


@router.patch("/{empl_skill_id}", response_model=EmployeeSkillOut)
def patch_employee_skill(
    empl_skill_id: uuid.UUID,
    payload: EmployeeSkillUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("skills", "update")),
) -> EmployeeSkillOut:
    """사원기술 연결 수정 — 전달된 필드만 갱신"""
    employee_skill = get_employee_skill(db, empl_skill_id)
    if employee_skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원기술 연결 정보를 찾을 수 없습니다.")

    before_snapshot = EmployeeSkillOut.model_validate(employee_skill).model_dump(mode="json")
    try:
        employee_skill = update_employee_skill(db, employee_skill, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 사원-기술 조합이거나 사원/기술 ID가 유효하지 않습니다.",
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee_skill.EMPL_SKILL_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=EmployeeSkillOut.model_validate(employee_skill).model_dump(mode="json"),
    )
    return employee_skill
