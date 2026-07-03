from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.repositories.codes import list_departments, list_job_types, list_positions
from app.schemas.hr_dept_mst import DepartmentOut
from app.schemas.hr_jikgup_mst import PositionOut
from app.schemas.hr_jikmu_mst import JobTypeOut

# HR_DEPT_MST/HR_JIKGUP_MST/HR_JIKMU_MST 코드 마스터 조회 API (로드맵 §8 다음 작업 1번).
# 세 테이블 모두 등록/수정 화면(§4 Phase 4)이 별도이므로 이 라우터는 조회만 다룬다.
#
# 권한: 부서/직급은 운영팀 확인 결과(2026-07-03) 독립 화면이 아닌 "공통 코드/기준정보"로
# 취급하기로 확정되어 `codes` 화면 키(전 역할 view 허용)로 보호한다. 직무 유형(`job_types`)
# 조회도 화면 필터/옵션 목적으로 전 역할이 조회할 수 있어야 하므로 동일하게 `codes.view`
# 정책을 적용한다 — 단, 직무 유형 관리 화면의 등록/수정/삭제(§8 다음 작업 별도 항목, 아직
# 미구현)는 기존 `job_types.create/update/delete`(ADMIN/HR_MGR 전용) 권한을 그대로 유지한다.
router = APIRouter(tags=["codes"])


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
