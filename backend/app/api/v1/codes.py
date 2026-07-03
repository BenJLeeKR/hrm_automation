import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.codes import (
    create_job_type,
    get_job_type,
    list_departments,
    list_job_types,
    list_positions,
    update_job_type,
)
from app.schemas.hr_dept_mst import DepartmentOut
from app.schemas.hr_jikgup_mst import PositionOut
from app.schemas.hr_jikmu_mst import JobTypeCreate, JobTypeOut, JobTypeUpdate

# HR_DEPT_MST/HR_JIKGUP_MST 코드 마스터 조회 API (로드맵 §8 다음 작업 1번) + 직무 유형
# 관리(SCR-006, HR_JIKMU_MST) 조회/등록/수정 API. 부서/직급은 등록/수정 화면이 아직 없어
# 이 라우터가 조회만 다루지만, 직무 유형은 이번에 등록/수정 엔드포인트를 함께 추가한다.
#
# 권한: 부서/직급은 운영팀 확인 결과(2026-07-03) 독립 화면이 아닌 "공통 코드/기준정보"로
# 취급하기로 확정되어 `codes` 화면 키(전 역할 view 허용)로 보호한다. 직무 유형(`job_types`)
# 조회도 화면 필터/옵션 목적으로 전 역할이 조회할 수 있어야 하므로 동일하게 `codes.view`
# 정책을 적용한다 — 단, 직무 유형 관리 화면의 등록/수정/삭제는 `job_types.create/update`
# (ADMIN/HR_MGR 전용) 권한으로 보호한다(`PERMISSION_MATRIX.md` "job_types" 섹션 참조).
router = APIRouter(tags=["codes"])

_TGT_TBL_NM = "HR_JIKMU_MST"


@router.get(
    "/departments", response_model=list[DepartmentOut], dependencies=[Depends(require_permission("codes", "view"))]
)
def get_departments(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 부서만)"),
    db: Session = Depends(get_db),
) -> list[DepartmentOut]:
    """부서 코드 목록 조회"""
    return list_departments(db, use_yn=use_yn)


@router.get(
    "/positions", response_model=list[PositionOut], dependencies=[Depends(require_permission("codes", "view"))]
)
def get_positions(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 직급만)"),
    db: Session = Depends(get_db),
) -> list[PositionOut]:
    """직급 코드 목록 조회"""
    return list_positions(db, use_yn=use_yn)


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
        tgt_tbl_nm=_TGT_TBL_NM,
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
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=job_type.JIKMU_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=JobTypeOut.model_validate(job_type).model_dump(mode="json"),
    )
    return job_type
