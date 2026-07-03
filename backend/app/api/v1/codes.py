from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.codes import list_departments, list_job_types, list_positions
from app.schemas.hr_dept_mst import DepartmentOut
from app.schemas.hr_jikgup_mst import PositionOut
from app.schemas.hr_jikmu_mst import JobTypeOut

# HR_DEPT_MST/HR_JIKGUP_MST/HR_JIKMU_MST 코드 마스터 조회 API (로드맵 §8 다음 작업 1번).
# 세 테이블 모두 등록/수정 화면(§4 Phase 4)이 별도이므로 이 라우터는 조회만 다룬다.
router = APIRouter(tags=["codes"])


@router.get("/departments", response_model=list[DepartmentOut])
def get_departments(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 부서만)"),
    db: Session = Depends(get_db),
) -> list[DepartmentOut]:
    """부서 코드 목록 조회"""
    return list_departments(db, use_yn=use_yn)


@router.get("/positions", response_model=list[PositionOut])
def get_positions(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 직급만)"),
    db: Session = Depends(get_db),
) -> list[PositionOut]:
    """직급 코드 목록 조회"""
    return list_positions(db, use_yn=use_yn)


@router.get("/job-types", response_model=list[JobTypeOut])
def get_job_types(
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 직무만)"),
    db: Session = Depends(get_db),
) -> list[JobTypeOut]:
    """직무 유형 코드 목록 조회"""
    return list_job_types(db, use_yn=use_yn)
