import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.repositories.hr_empl_role_rel import list_employee_roles
from app.schemas.hr_empl_role_rel import EmployeeRoleOut

# 사원역할 연결(HR_EMPL_ROLE_REL) 조회 전용 API — 사원 목록/상세 화면의 "보유 역할" 배지
# 표시용(로드맵 §8 "사원 목록 화면 실 API 연동"). 등록/수정은 아직 화면·요구사항이 없어
# 이번 범위에서 다루지 않는다 — 조회 화면(employees, employees/skills)과 동일한
# `employees.view` 권한으로 보호한다.
router = APIRouter(prefix="/employee-roles", tags=["employee-roles"])


@router.get(
    "", response_model=list[EmployeeRoleOut], dependencies=[Depends(require_permission("employees", "view"))]
)
def get_employee_roles(
    empl_id: uuid.UUID | None = Query(None, description="사원 ID로 필터링 (HR_EMPL_MST.EMPL_ID)"),
    db: Session = Depends(get_db),
) -> list[EmployeeRoleOut]:
    """사원역할 연결 목록 조회"""
    return list_employee_roles(db, empl_id=empl_id)
