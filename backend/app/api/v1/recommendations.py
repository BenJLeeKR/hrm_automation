import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.pjt_rcmd_rslt import list_recommendation_results, run_recommendation
from app.repositories.pjt_rsrc_req import create_resource_request, get_resource_request
from app.schemas.pjt_rcmd_rslt import RecommendationResultOut
from app.schemas.pjt_rsrc_req import ResourceRequestCreate, ResourceRequestOut

router = APIRouter(tags=["recommendations"])

_RSRC_REQ_TGT_TBL_NM = "PJT_RSRC_REQ"


class RecommendationScoreRequest(BaseModel):
    """추천 실행 요청 스키마 (`POST /api/v1/recommendations/score`) — 앞서 등록한
    리소스 요청(`REQ_ID`)을 대상으로 점수를 계산한다."""

    req_id: uuid.UUID


@router.post(
    "/resource-requests", response_model=ResourceRequestOut, status_code=status.HTTP_201_CREATED
)
def post_resource_request(
    payload: ResourceRequestCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("recommendations", "create")),
) -> ResourceRequestOut:
    """리소스 요청 등록 (SCR-011 "추천 조건 입력" — 로드맵 §8 다음 작업 1번)"""
    try:
        resource_request = create_resource_request(
            db, {**payload.model_dump(), "REQ_USER_ID": current_user.USER_ID}
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="프로젝트/직무 유형 ID가 유효하지 않습니다."
        ) from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_RSRC_REQ_TGT_TBL_NM,
        tgt_id=resource_request.REQ_ID,
        aft_val_json=ResourceRequestOut.model_validate(resource_request).model_dump(mode="json"),
    )
    return resource_request


@router.post("/recommendations/score", response_model=list[RecommendationResultOut])
def post_recommendation_score(
    payload: RecommendationScoreRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("recommendations", "create")),
) -> list[RecommendationResultOut]:
    """점수 기반 후보 추천 실행 (SCR-011 "추천 실행" — 로드맵 §8 다음 작업 1번).

    직무 유형 15%·기술 매칭 35%·숙련도 25%·가동 가능일 15%·유사 경험 7%·역할 적합도 3%
    가중치(`app/repositories/pjt_rcmd_rslt.py` 참조)로 재직 사원 전체를 채점해 상위
    10명을 `PJT_RCMD_RSLT`에 저장한다. 동일 요청으로 재실행하면 이전 결과를 덮어쓴다.
    """
    resource_request = get_resource_request(db, payload.req_id)
    if resource_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="리소스 요청을 찾을 수 없습니다.")

    results = run_recommendation(db, resource_request, as_of=date.today())

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm="PJT_RCMD_RSLT",
        tgt_id=payload.req_id,
        aft_val_json={"candidate_count": len(results)},
    )
    return results


@router.get("/recommendations/{req_id}", response_model=list[RecommendationResultOut])
def get_recommendation_results(
    req_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("recommendations", "view")),
) -> list[RecommendationResultOut]:
    """이전 추천 결과 조회 (SCR-011 "연동 API")"""
    resource_request = get_resource_request(db, req_id)
    if resource_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="리소스 요청을 찾을 수 없습니다.")

    return list_recommendation_results(db, req_id)
