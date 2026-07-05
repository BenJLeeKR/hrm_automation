import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_jikgup_mst import HrJikgupMst
from app.models.hr_jikmu_mst import HrJikmuMst

# HR_DEPT_MST/HR_JIKGUP_MST/HR_JIKMU_MST는 모두 소규모 코드 마스터 테이블이라 §8 다음 작업
# 백로그 항목("부서/직급/직무 코드 조회 API")과 동일하게 하나의 모듈에 묶어 구현한다.

_ACTIVE_EMPL_STAT_CD = "ACTIVE"


def list_departments(db: Session, *, use_yn: bool | None = True) -> list[HrDeptMst]:
    """부서 목록 조회 — 정렬 순서(DEPT_ORD) 기준. `use_yn=None`이면 비활성 부서도 포함."""
    stmt = select(HrDeptMst)
    if use_yn is not None:
        stmt = stmt.where(HrDeptMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrDeptMst.DEPT_ORD)))


def get_department(db: Session, dept_id: uuid.UUID) -> HrDeptMst | None:
    return db.get(HrDeptMst, dept_id)


def create_department(db: Session, data: dict) -> HrDeptMst:
    """부서 등록 (설계서 §6.4 "부서/직급 코드" — 전용 화면 없이 Admin이 Swagger에서 직접
    호출). `DEPT_CD` UNIQUE 위반은 호출부(API 라우터)에서 `IntegrityError`를 잡아 처리한다."""
    dept = HrDeptMst(**data)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


def update_department(db: Session, dept: HrDeptMst, data: dict) -> HrDeptMst:
    """전달된 필드만 갱신 (부분 업데이트). `USE_YN=FALSE` 비활성 보호(재직 사원 존재 시 409)는
    호출부(API 라우터)에서 `count_active_employees_by_dept`로 사전 검증한다."""
    for key, value in data.items():
        setattr(dept, key, value)
    db.commit()
    db.refresh(dept)
    return dept


def count_active_employees_by_dept(db: Session, dept_id: uuid.UUID) -> int:
    """해당 부서에 재직 중(`EMPL_STAT_CD='ACTIVE'`)인 사원 수 (설계서 §5.5 "부서 비활성 보호")."""
    stmt = select(func.count()).select_from(HrEmplMst).where(
        HrEmplMst.DEPT_ID == dept_id, HrEmplMst.EMPL_STAT_CD == _ACTIVE_EMPL_STAT_CD
    )
    return db.scalar(stmt) or 0


def list_positions(db: Session, *, use_yn: bool | None = True) -> list[HrJikgupMst]:
    """직급 목록 조회 — 정렬 순서(JIKGUP_ORD) 기준. `use_yn=None`이면 비활성 직급도 포함."""
    stmt = select(HrJikgupMst)
    if use_yn is not None:
        stmt = stmt.where(HrJikgupMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrJikgupMst.JIKGUP_ORD)))


def get_position(db: Session, jikgup_id: uuid.UUID) -> HrJikgupMst | None:
    return db.get(HrJikgupMst, jikgup_id)


def create_position(db: Session, data: dict) -> HrJikgupMst:
    """직급 등록 (설계서 §6.4 "부서/직급 코드" — 전용 화면 없이 Admin이 Swagger에서 직접
    호출). `JIKGUP_CD` UNIQUE 위반은 호출부(API 라우터)에서 `IntegrityError`를 잡아 처리한다."""
    position = HrJikgupMst(**data)
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


def update_position(db: Session, position: HrJikgupMst, data: dict) -> HrJikgupMst:
    """전달된 필드만 갱신 (부분 업데이트). `USE_YN=FALSE` 비활성 보호(재직 사원 존재 시 409)는
    호출부(API 라우터)에서 `count_active_employees_by_jikgup`로 사전 검증한다."""
    for key, value in data.items():
        setattr(position, key, value)
    db.commit()
    db.refresh(position)
    return position


def count_active_employees_by_jikgup(db: Session, jikgup_id: uuid.UUID) -> int:
    """해당 직급에 재직 중(`EMPL_STAT_CD='ACTIVE'`)인 사원 수 (설계서 §5.5 "직급 비활성 보호")."""
    stmt = select(func.count()).select_from(HrEmplMst).where(
        HrEmplMst.JIKGUP_ID == jikgup_id, HrEmplMst.EMPL_STAT_CD == _ACTIVE_EMPL_STAT_CD
    )
    return db.scalar(stmt) or 0


def list_job_types(db: Session, *, use_yn: bool | None = True) -> list[HrJikmuMst]:
    """직무 유형 목록 조회 — 정렬 순서(SORT_ORD) 기준. `use_yn=None`이면 비활성 직무도 포함."""
    stmt = select(HrJikmuMst)
    if use_yn is not None:
        stmt = stmt.where(HrJikmuMst.USE_YN == use_yn)
    return list(db.scalars(stmt.order_by(HrJikmuMst.SORT_ORD)))


def get_job_type(db: Session, jikmu_id: uuid.UUID) -> HrJikmuMst | None:
    return db.get(HrJikmuMst, jikmu_id)


def create_job_type(db: Session, data: dict) -> HrJikmuMst:
    """직무 유형 등록 (SCR-006). `JIKMU_CD` UNIQUE 위반은 호출부(API 라우터)에서
    `sqlalchemy.exc.IntegrityError`를 잡아 처리한다."""
    job_type = HrJikmuMst(**data)
    db.add(job_type)
    db.commit()
    db.refresh(job_type)
    return job_type


def update_job_type(db: Session, job_type: HrJikmuMst, data: dict) -> HrJikmuMst:
    """전달된 필드만 갱신 (부분 업데이트)."""
    for key, value in data.items():
        setattr(job_type, key, value)
    db.commit()
    db.refresh(job_type)
    return job_type
