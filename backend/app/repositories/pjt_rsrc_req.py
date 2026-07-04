import uuid

from sqlalchemy.orm import Session

from app.models.pjt_rsrc_req import PjtRsrcReq


def get_resource_request(db: Session, req_id: uuid.UUID) -> PjtRsrcReq | None:
    return db.get(PjtRsrcReq, req_id)


def create_resource_request(db: Session, data: dict) -> PjtRsrcReq:
    """리소스 요청 등록. `PJT_ID`/`REQ_JIKMU_ID` FK 위반은 호출부(API 라우터)에서
    `sqlalchemy.exc.IntegrityError`를 잡아 처리한다."""
    request = PjtRsrcReq(**data, REQ_STAT_CD="OPEN")
    db.add(request)
    db.commit()
    db.refresh(request)
    return request
