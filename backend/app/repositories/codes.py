from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_jikgup_mst import HrJikgupMst
from app.models.hr_jikmu_mst import HrJikmuMst

# HR_DEPT_MST/HR_JIKGUP_MST/HR_JIKMU_MST는 모두 소규모 코드 마스터 테이블이라 §8 다음 작업
# 백로그 항목("부서/직급/직무 코드 조회 API")과 동일하게 하나의 모듈에 묶어 구현한다.


def list_departments(db: Session, *, use_yn: bool | None = True) -> list[HrDeptMst]:
    """부서 목록 조회 — 정렬 순서(DEPT_ORD) 기준. `use_yn=None`이면 비활성 부서도 포함."""
    stmt = select(HrDeptMst)
    if use_yn is not None:
        stmt = stmt.where(HrDeptMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrDeptMst.DEPT_ORD)))


def list_positions(db: Session, *, use_yn: bool | None = True) -> list[HrJikgupMst]:
    """직급 목록 조회 — 정렬 순서(JIKGUP_ORD) 기준. `use_yn=None`이면 비활성 직급도 포함."""
    stmt = select(HrJikgupMst)
    if use_yn is not None:
        stmt = stmt.where(HrJikgupMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrJikgupMst.JIKGUP_ORD)))


def list_job_types(db: Session, *, use_yn: bool | None = True) -> list[HrJikmuMst]:
    """직무 유형 목록 조회 — 정렬 순서(SORT_ORD) 기준. `use_yn=None`이면 비활성 직무도 포함."""
    stmt = select(HrJikmuMst)
    if use_yn is not None:
        stmt = stmt.where(HrJikmuMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrJikmuMst.SORT_ORD)))
