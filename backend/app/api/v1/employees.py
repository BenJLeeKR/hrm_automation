import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.hr_empl_mst import create_employee, get_employee, list_employees, update_employee
from app.schemas.hr_empl_mst import EmployeeCreate, EmployeeListResponse, EmployeeOut, EmployeeUpdate

_TGT_TBL_NM = "HR_EMPL_MST"

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=EmployeeListResponse, dependencies=[Depends(require_permission("employees", "view"))])
def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    dept_id: uuid.UUID | None = Query(None, description="부서 ID로 필터링 (HR_DEPT_MST.DEPT_ID)"),
    jikmu_id: uuid.UUID | None = Query(None, description="직무 유형 ID로 필터링 (HR_JIKMU_MST.JIKMU_ID)"),
    empl_stat_cd: str | None = Query(None, description="재직 상태 코드 (ACTIVE/LEAVE/RETIRED)"),
    db: Session = Depends(get_db),
) -> EmployeeListResponse:
    """사원 목록 조회 (로드맵 §8 다음 작업 7번)"""
    items, total = list_employees(
        db, skip=skip, limit=limit, dept_id=dept_id, jikmu_id=jikmu_id, empl_stat_cd=empl_stat_cd
    )
    return EmployeeListResponse(total=total, skip=skip, limit=limit, items=items)


@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def post_employee(
    payload: EmployeeCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "create")),
) -> EmployeeOut:
    """사원 등록 (로드맵 §8 다음 작업 8번)"""
    try:
        employee = create_employee(db, payload.model_dump())
    except IntegrityError:
        # EMPL_NO/EMAIL_ADDR UNIQUE 위반 또는 DEPT_ID/JIKGUP_ID/JIKMU_ID FK 위반
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="사번/이메일 중복이거나 부서·직급·직무 ID가 유효하지 않습니다.",
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee.EMPL_ID,
        aft_val_json=EmployeeOut.model_validate(employee).model_dump(mode="json"),
    )
    return employee


@router.patch("/{empl_id}", response_model=EmployeeOut)
def patch_employee(
    empl_id: uuid.UUID,
    payload: EmployeeUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("employees", "update")),
) -> EmployeeOut:
    """사원 수정 (로드맵 §8 다음 작업 8번) — 전달된 필드만 갱신"""
    employee = get_employee(db, empl_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원을 찾을 수 없습니다.")

    before_snapshot = EmployeeOut.model_validate(employee).model_dump(mode="json")
    try:
        employee = update_employee(db, employee, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="사번/이메일 중복이거나 부서·직급·직무 ID가 유효하지 않습니다.",
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=employee.EMPL_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=EmployeeOut.model_validate(employee).model_dump(mode="json"),
    )
    return employee
