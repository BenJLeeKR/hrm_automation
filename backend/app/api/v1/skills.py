import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.hr_skill_mst import create_skill, get_skill, list_skills, update_skill
from app.schemas.hr_skill_mst import SkillCreate, SkillOut, SkillUpdate

router = APIRouter(prefix="/skills", tags=["skills"])

_TGT_TBL_NM = "HR_SKILL_MST"


@router.get("", response_model=list[SkillOut], dependencies=[Depends(require_permission("skills", "view"))])
def get_skills(
    skill_grp_cd: str | None = Query(None, description="기술 그룹 코드로 필터링 (BACKEND/FRONTEND 등)"),
    use_yn: bool | None = Query(True, description="사용 여부 필터 — 생략 시 True(사용 중인 기술만)"),
    db: Session = Depends(get_db),
) -> list[SkillOut]:
    """기술 목록 조회 (로드맵 §8 다음 작업 1번)"""
    return list_skills(db, skill_grp_cd=skill_grp_cd, use_yn=use_yn)


@router.post("", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def post_skill(
    payload: SkillCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("skills", "create")),
) -> SkillOut:
    """기술 등록"""
    try:
        skill = create_skill(db, payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 기술입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="CREATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=skill.SKILL_ID,
        aft_val_json=SkillOut.model_validate(skill).model_dump(mode="json"),
    )
    return skill


@router.patch("/{skill_id}", response_model=SkillOut)
def patch_skill(
    skill_id: uuid.UUID,
    payload: SkillUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("skills", "update")),
) -> SkillOut:
    """기술 수정 — 전달된 필드만 갱신"""
    skill = get_skill(db, skill_id)
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="기술을 찾을 수 없습니다.")

    before_snapshot = SkillOut.model_validate(skill).model_dump(mode="json")
    try:
        skill = update_skill(db, skill, payload.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 기술입니다.") from None

    record_audit(
        db,
        request,
        current_user,
        act_cd="UPDATE",
        tgt_tbl_nm=_TGT_TBL_NM,
        tgt_id=skill.SKILL_ID,
        bfr_val_json=before_snapshot,
        aft_val_json=SkillOut.model_validate(skill).model_dump(mode="json"),
    )
    return skill
