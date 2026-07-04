import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.repositories.hr_avail_snap import compute_availability, list_availability
from app.repositories.hr_empl_mst import get_employee
from app.schemas.hr_avail_snap import AvailabilityCalcOut

router = APIRouter(prefix="/availability", tags=["availability"])


@router.get(
    "",
    response_model=list[AvailabilityCalcOut],
    dependencies=[Depends(require_permission("availability", "view"))],
)
def get_availability_list(
    jikmu_id: uuid.UUID | None = Query(None, description="직무 유형 ID로 필터링 (HR_JIKMU_MST.JIKMU_ID)"),
    dept_id: uuid.UUID | None = Query(None, description="부서 ID로 필터링 (HR_DEPT_MST.DEPT_ID)"),
    skill_id: uuid.UUID | None = Query(None, description="기술 ID로 필터링 (HR_SKILL_MST.SKILL_ID)"),
    min_prfcy_levl: int | None = Query(
        None, ge=1, le=5, description="최소 숙련도(1~5) — skill_id와 함께 사용, 단독 지정 시 무시됨"
    ),
    snap_dt: date | None = Query(None, description="기준일 — 생략 시 오늘 날짜"),
    db: Session = Depends(get_db),
) -> list[AvailabilityCalcOut]:
    """재직 사원 전체 가동률 일괄 조회 (로드맵 §8 다음 작업 1번, SCR-010 "가동 가능 인력").

    `GET /availability/{empl_id}`(단건)와 동일한 즉시 계산 로직을 재직 사원 전체에
    적용한다 — `HR_AVAIL_SNAP` 테이블에는 저장하지 않는다. `skill_id`/`min_prfcy_levl`은
    직무 유형·부서 필터에 이어 기술·숙련도 조건까지 복합 적용하기 위한 필터다.
    """
    results = list_availability(
        db,
        snap_dt=snap_dt or date.today(),
        jikmu_id=jikmu_id,
        dept_id=dept_id,
        skill_id=skill_id,
        min_prfcy_levl=min_prfcy_levl,
    )
    return [AvailabilityCalcOut(**result.__dict__) for result in results]


@router.get(
    "/{empl_id}",
    response_model=AvailabilityCalcOut,
    dependencies=[Depends(require_permission("availability", "view"))],
)
def get_employee_availability(
    empl_id: uuid.UUID,
    snap_dt: date | None = Query(None, description="기준일 — 생략 시 오늘 날짜"),
    db: Session = Depends(get_db),
) -> AvailabilityCalcOut:
    """사원 가동률 즉시 계산 (로드맵 §8 다음 작업 1번, `backend/docs/AVAILABILITY_CALC_SPEC.md` §2/§4 기준).

    `HR_AVAIL_SNAP` 스냅샷 행을 생성하지 않는 즉시 계산 API다 — 매일 01:00 배치
    `HR_AVAIL_SNAP_GEN`(Phase 7, 미구현)이 스냅샷 저장을 전담하므로 중복 저장하지 않는다.
    """
    employee = get_employee(db, empl_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사원을 찾을 수 없습니다.")

    result = compute_availability(db, empl_id=empl_id, snap_dt=snap_dt or date.today())
    return AvailabilityCalcOut(**result.__dict__)
