import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.pjt_mst import PjtMst


def list_projects(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    pjt_stat_cd: str | None = None,
) -> tuple[list[PjtMst], int]:
    """프로젝트 목록 조회 — 진행 상태 필터, skip/limit 페이지네이션."""
    stmt = select(PjtMst)
    count_stmt = select(func.count()).select_from(PjtMst)

    if pjt_stat_cd is not None:
        stmt = stmt.where(PjtMst.PJT_STAT_CD == pjt_stat_cd)
        count_stmt = count_stmt.where(PjtMst.PJT_STAT_CD == pjt_stat_cd)

    total = db.scalar(count_stmt) or 0
    items = list(db.scalars(stmt.order_by(PjtMst.PJT_CD).offset(skip).limit(limit)))
    return items, total


def get_project(db: Session, pjt_id: uuid.UUID) -> PjtMst | None:
    return db.get(PjtMst, pjt_id)


def create_project(db: Session, data: dict) -> PjtMst:
    """프로젝트 등록. `PJT_CD` UNIQUE 위반은 호출부(API 라우터)에서
    `sqlalchemy.exc.IntegrityError`를 잡아 처리한다."""
    project = PjtMst(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project: PjtMst, data: dict) -> PjtMst:
    """전달된 필드만 갱신 (부분 업데이트)."""
    for field, value in data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project
