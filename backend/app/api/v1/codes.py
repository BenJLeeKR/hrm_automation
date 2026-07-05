import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.codes import (
    count_active_employees_by_dept,
    count_active_employees_by_jikgup,
    create_department,
    create_job_type,
    create_position,
    get_department,
    get_job_type,
    get_position,
    list_departments,
    list_job_types,
    list_positions,
    update_department,
    update_job_type,
    update_position,
)
from app.schemas.hr_dept_mst import DepartmentCreate, DepartmentOut, DepartmentUpdate
from app.schemas.hr_jikgup_mst import PositionCreate, PositionOut, PositionUpdate
from app.schemas.hr_jikmu_mst import JobTypeCreate, JobTypeOut, JobTypeUpdate

# HR_DEPT_MST/HR_JIKGUP_MST 코드 마스터 조회/등록/수정 API (로드맵 §8 다음 작업 1번, §9-1
# "부서/직급 등록·수정 API 없음" 해소) + 직무 유형 관리(SCR-006, HR_JIKMU_MST) 조회/등록/
# 수정 API.
#
# 권한: 부서/직급은 운영팀 확인 결과(2026-07-03) 독립 화면이 아닌 "공통 코드/기준정보"로
# 취급하기로 확정되어 `codes` 화면 키로 보호한다 — `view`는 전 역할 허용, `create`/`update`는
# ADMIN/HR_MGR만 허용(설계서 §6.4 "전용 관리 화면 없음" — Admin이 `/docs`(Swagger UI)에서
# 직접 호출하는 용도이며, 프론트엔드 전용 화면은 만들지 않는다). 직무 유형(`job_types`)
# 조회도 화면 필터/옵션 목적으로 전 역할이 조회할 수 있어야 하므로 동일하게 `codes.view`
# 정책을 적용한다 — 단, 직무 유형 관리 화면의 등록/수정/삭제는 `job_types.create/update`
# (ADMIN/HR_MGR 전용) 권한으로 보호한다(`PERMISSION_MATRIX.md` "job_types" 섹션 참조).
router = APIRouter(tags=["codes"])

_TGT_TBL_NM_DEPT = "HR_DEPT_MST"
_TGT_TBL_NM_JIKGUP = "HR_JIKGUP_MST"
_TGT_TBL_NM_JIKMU = "HR_JIKMU_MST"


@router.get(
    "/departments", response_model=list[DepartmentOut], dependencies=[Depends(require_permission("codes", "view"))]
)
def get_departments(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 부서만)"),
    db: Session = Depends(get_db),
) -> list[DepartmentOut]:
    """부서 코드 목록 조회"""
    return list_departments(db, use_yn=use_yn)


@router.post("/departments", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def post_department(
    payload: DepartmentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("codes", "create")),
) -> DepartmentOut:
    """부서 등록 (설계서 §6.4 "부서/직급 코드" — 전용 화면 없이 Admin이 Swagger에서 직접
    호출, §9-1 "부서/직급 등록·수정 API 없음" 해소)"""
    try:
        dept = create_department(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 부서 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM_DEPT,
        tgt_id=dept.DEPT_ID,
        aft_val_json=DepartmentOut.model_validate(dept).model_dump(mode="json"),
    )
    return dept


@router.patch("/departments/{dept_id}", response_model=DepartmentOut)
def patch_department(
    dept_id: uuid.UUID,
    payload: DepartmentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("codes", "update")),
) -> DepartmentOut:
    """부서 수정 — 전달된 필드만 갱신. `USE_YN=FALSE` 요청은 재직 중인 사원이 있으면 409로
    거부한다(설계서 §5.5 "부서 비활성 보호", §9-1 해소)"""
    dept = get_department(db, dept_id)
    if dept is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="부서를 찾을 수 없습니다.")

    data = payload.model_dump(exclude_unset=True)
    if data.get("USE_YN") is False and count_active_employees_by_dept(db, dept_id) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="해당 부서에 재직 중인 사원이 있어 비활성 처리할 수 없습니다."
        )

    before_snapshot = DepartmentOut.model_validate(dept).model_dump(mode="json")
    try:
        dept = update_department(db, dept, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 부서 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM_DEPT,
        tgt_id=dept.DEPT_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=DepartmentOut.model_validate(dept).model_dump(mode="json"),
    )
    return dept


@router.get(
    "/positions", response_model=list[PositionOut], dependencies=[Depends(require_permission("codes", "view"))]
)
def get_positions(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 직급만)"),
    db: Session = Depends(get_db),
) -> list[PositionOut]:
    """직급 코드 목록 조회"""
    return list_positions(db, use_yn=use_yn)


@router.post("/positions", response_model=PositionOut, status_code=status.HTTP_201_CREATED)
def post_position(
    payload: PositionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("codes", "create")),
) -> PositionOut:
    """직급 등록 (설계서 §6.4 "부서/직급 코드" — 전용 화면 없이 Admin이 Swagger에서 직접
    호출, §9-1 "부서/직급 등록·수정 API 없음" 해소)"""
    try:
        position = create_position(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 직급 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM_JIKGUP,
        tgt_id=position.JIKGUP_ID,
        aft_val_json=PositionOut.model_validate(position).model_dump(mode="json"),
    )
    return position


@router.patch("/positions/{jikgup_id}", response_model=PositionOut)
def patch_position(
    jikgup_id: uuid.UUID,
    payload: PositionUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("codes", "update")),
) -> PositionOut:
    """직급 수정 — 전달된 필드만 갱신. `USE_YN=FALSE` 요청은 재직 중인 사원이 있으면 409로
    거부한다(설계서 §5.5 "직급 비활성 보호", §9-1 해소)"""
    position = get_position(db, jikgup_id)
    if position is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="직급을 찾을 수 없습니다.")

    data = payload.model_dump(exclude_unset=True)
    if data.get("USE_YN") is False and count_active_employees_by_jikgup(db, jikgup_id) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="해당 직급의 재직 중인 사원이 있어 비활성 처리할 수 없습니다."
        )

    before_snapshot = PositionOut.model_validate(position).model_dump(mode="json")
    try:
        position = update_position(db, position, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 직급 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM_JIKGUP,
        tgt_id=position.JIKGUP_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=PositionOut.model_validate(position).model_dump(mode="json"),
    )
    return position


@router.get(
    "/job-types", response_model=list[JobTypeOut], dependencies=[Depends(require_permission("codes", "view"))]
)
def get_job_types(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 직무만)"),
    db: Session = Depends(get_db),
) -> list[JobTypeOut]:
    """직무 유형 코드 목록 조회"""
    return list_job_types(db, use_yn=use_yn)


@router.post(
    "/job-types", response_model=JobTypeOut, status_code=status.HTTP_201_CREATED
)
def post_job_type(
    payload: JobTypeCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("job_types", "create")),
) -> JobTypeOut:
    """직무 유형 등록 (SCR-006, 로드맵 §8 다음 작업 1번)"""
    try:
        job_type = create_job_type(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 직무 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM_JIKMU,
        tgt_id=job_type.JIKMU_ID,
        aft_val_json=JobTypeOut.model_validate(job_type).model_dump(mode="json"),
    )
    return job_type


@router.patch("/job-types/{jikmu_id}", response_model=JobTypeOut)
def patch_job_type(
    jikmu_id: uuid.UUID,
    payload: JobTypeUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("job_types", "update")),
) -> JobTypeOut:
    """직무 유형 수정 — 전달된 필드만 갱신 (SCR-006, 로드맵 §8 다음 작업 1번)"""
    job_type = get_job_type(db, jikmu_id)
    if job_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="직무 유형을 찾을 수 없습니다.")

    before_snapshot = JobTypeOut.model_validate(job_type).model_dump(mode="json")
    try:
        job_type = update_job_type(db, job_type, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 등록된 직무 코드입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM_JIKMU,
        tgt_id=job_type.JIKMU_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=JobTypeOut.model_validate(job_type).model_dump(mode="json"),
    )
    return job_type
