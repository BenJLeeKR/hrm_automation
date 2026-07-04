import uuid
from dataclasses import dataclass, field
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_rcmd_rslt import PjtRcmdRslt
from app.models.pjt_rsrc_req import PjtRsrcReq
from app.repositories.hr_avail_snap import list_availability

# 추천 점수 산정 가중치 (설계서 SCR-011, `pjt_rcmd_rslt.py` 모델 주석 참조) — 6개 항목 합 100점.
# 설계서에는 가중치 비율만 명시되어 있고 항목별 세부 산정 공식은 없어(§9 리스크 참고),
# 아래 각 함수의 계산 방식은 MVP 해석이다 — 운영팀 확정 전까지 이 기준을 유지한다.
_WEIGHT_JOB_MATCH = 15
_WEIGHT_SKILL_MATCH = 35
_WEIGHT_PROFICIENCY = 25
_WEIGHT_AVAILABILITY = 15
_WEIGHT_EXPERIENCE = 7
_WEIGHT_ROLE_FIT = 3
_TOP_N = 10  # 설계서 레이아웃 "총 N명 후보 중 상위 10명 표시" 기준


@dataclass
class ScoredCandidate:
    EMPL_ID: uuid.UUID
    TOT_SCORE: float
    SCORE_DTL_JSON: dict = field(default_factory=dict)
    RCMD_RSN: str = ""


def _score_candidates(db: Session, request: PjtRsrcReq, *, as_of: date) -> list[ScoredCandidate]:
    """재직 사원 전체를 대상으로 요청 조건 대비 적합도 점수를 계산한다."""
    req_skill_ids = {uuid.UUID(s) for s in request.REQ_SKILL_JSON.get("SKILL_IDS", [])}
    min_prfcy = request.REQ_SKILL_JSON.get("MIN_PRFCY_LEVL")

    employees = list(db.scalars(select(HrEmplMst).where(HrEmplMst.EMPL_STAT_CD == "ACTIVE")))
    if not employees:
        return []
    employee_ids = [e.EMPL_ID for e in employees]

    empl_skills_by_id: dict[uuid.UUID, list[HrEmplSkillRel]] = {empl_id: [] for empl_id in employee_ids}
    for rel in db.scalars(select(HrEmplSkillRel).where(HrEmplSkillRel.EMPL_ID.in_(employee_ids))):
        empl_skills_by_id[rel.EMPL_ID].append(rel)

    # 유사경험/역할적합도 산정용 — 사원별 과거(DONE) 투입 이력의 역할명·직무 매칭 여부를 본다
    past_assignments_by_id: dict[uuid.UUID, list[PjtAsgnHis]] = {empl_id: [] for empl_id in employee_ids}
    for asgn in db.scalars(
        select(PjtAsgnHis).where(PjtAsgnHis.EMPL_ID.in_(employee_ids), PjtAsgnHis.ASGN_STAT_CD == "DONE")
    ):
        past_assignments_by_id[asgn.EMPL_ID].append(asgn)

    availability_by_id = {a.EMPL_ID: a for a in list_availability(db, snap_dt=as_of)}

    role_kw = request.REQ_ROLE_NM.strip().lower()
    results: list[ScoredCandidate] = []
    for employee in employees:
        detail: dict[str, float] = {}

        # 1) 직무 유형 일치 (15점) — REQ_JIKMU_ID 미지정 시 조건 없음으로 간주해 만점 부여
        if request.REQ_JIKMU_ID is None:
            job_score = _WEIGHT_JOB_MATCH
        else:
            job_score = _WEIGHT_JOB_MATCH if employee.JIKMU_ID == request.REQ_JIKMU_ID else 0
        detail["job_match"] = job_score

        # 2) 기술 매칭 (35점) — 요청 기술 중 보유 비율. 요청 기술 미지정 시 만점
        emp_skills = empl_skills_by_id.get(employee.EMPL_ID, [])
        emp_skill_ids = {s.SKILL_ID for s in emp_skills}
        if not req_skill_ids:
            skill_score = _WEIGHT_SKILL_MATCH
            matched_skill_ids = emp_skill_ids
        else:
            matched_skill_ids = req_skill_ids & emp_skill_ids
            skill_score = _WEIGHT_SKILL_MATCH * (len(matched_skill_ids) / len(req_skill_ids))
        detail["skill_match"] = round(skill_score, 2)

        # 3) 숙련도 (25점) — 매칭된 기술의 평균 숙련도(1~5) 비율. 매칭 기술이 없으면 0점
        matched_rels = [s for s in emp_skills if s.SKILL_ID in matched_skill_ids and s.PRFCY_LEVL is not None]
        if not req_skill_ids:
            prof_score = _WEIGHT_PROFICIENCY if not matched_rels else _WEIGHT_PROFICIENCY * (
                sum(s.PRFCY_LEVL for s in matched_rels) / len(matched_rels) / 5
            )
        elif matched_rels:
            avg_prfcy = sum(s.PRFCY_LEVL for s in matched_rels) / len(matched_rels)
            if min_prfcy is not None and avg_prfcy < min_prfcy:
                prof_score = 0.0  # 최소 숙련도 조건 미충족
            else:
                prof_score = _WEIGHT_PROFICIENCY * (avg_prfcy / 5)
        else:
            prof_score = 0.0
        detail["proficiency"] = round(prof_score, 2)

        # 4) 가동 가능일 (15점) — 희망 가동일 이내에 가동 가능하면 만점, 아니면 0점(이진 판정 MVP)
        avail = availability_by_id.get(employee.EMPL_ID)
        if avail is None:
            avail_score = 0.0
        elif avail.AVAIL_STAT_CD != "FULL":
            # AVAILABLE/PARTIAL은 오늘부터 가동 가능하므로 희망일 조건을 항상 충족
            avail_score = _WEIGHT_AVAILABILITY
        elif avail.AVAIL_STRT_DT is not None and avail.AVAIL_STRT_DT <= request.REQ_AVAIL_DT:
            avail_score = _WEIGHT_AVAILABILITY
        else:
            avail_score = 0.0
        detail["availability"] = avail_score

        # 5) 유사 경험 (7점) — 요청 역할명과 유사한 과거(DONE) 투입 이력 건수 기준(최대 3건=만점)
        similar_count = sum(
            1 for a in past_assignments_by_id.get(employee.EMPL_ID, []) if role_kw and role_kw in a.PRJT_ROLE_NM.lower()
        )
        exp_score = _WEIGHT_EXPERIENCE * min(similar_count, 3) / 3 if role_kw else _WEIGHT_EXPERIENCE
        detail["experience"] = round(exp_score, 2)

        # 6) 역할 적합도 (3점) — 과거 또는 현재 투입 이력에 동일 역할명이 있으면 만점
        role_fit_score = _WEIGHT_ROLE_FIT if similar_count > 0 else 0.0
        detail["role_fit"] = role_fit_score

        total = round(sum(detail.values()), 2)
        reason_parts = []
        if job_score == _WEIGHT_JOB_MATCH and request.REQ_JIKMU_ID is not None:
            reason_parts.append("직무 일치")
        if req_skill_ids and matched_skill_ids == req_skill_ids:
            reason_parts.append("기술 완전일치")
        elif matched_skill_ids:
            reason_parts.append("기술 일부 일치")
        if avail_score == _WEIGHT_AVAILABILITY:
            reason_parts.append("가동일 조건 충족")
        reason = ", ".join(reason_parts) if reason_parts else "기본 조건만 충족"

        results.append(ScoredCandidate(EMPL_ID=employee.EMPL_ID, TOT_SCORE=total, SCORE_DTL_JSON=detail, RCMD_RSN=reason))

    results.sort(key=lambda r: r.TOT_SCORE, reverse=True)
    return results


def run_recommendation(db: Session, request: PjtRsrcReq, *, as_of: date) -> list[PjtRcmdRslt]:
    """추천을 실행해 상위 후보를 `PJT_RCMD_RSLT`에 저장한다 (SCR-011 "추천 실행").

    같은 요청(`REQ_ID`)으로 재실행 시 이전 결과가 남지 않도록, 저장 전 기존 결과를
    먼저 삭제한다 — 추천은 매번 최신 데이터 기준으로 다시 계산하는 것이 설계 의도에
    맞다(과거 실행 이력 보관은 이번 범위에서 다루지 않음, §9 리스크 참고).
    """
    db.query(PjtRcmdRslt).filter(PjtRcmdRslt.REQ_ID == request.REQ_ID).delete()

    scored = _score_candidates(db, request, as_of=as_of)[:_TOP_N]
    rows = [
        PjtRcmdRslt(
            REQ_ID=request.REQ_ID,
            EMPL_ID=c.EMPL_ID,
            RCMD_RANK=rank,
            TOT_SCORE=c.TOT_SCORE,
            SCORE_DTL_JSON=c.SCORE_DTL_JSON,
            RCMD_RSN=c.RCMD_RSN,
        )
        for rank, c in enumerate(scored, start=1)
    ]
    db.add_all(rows)
    db.commit()
    for row in rows:
        db.refresh(row)
    return rows


def list_recommendation_results(db: Session, req_id: uuid.UUID) -> list[PjtRcmdRslt]:
    stmt = select(PjtRcmdRslt).where(PjtRcmdRslt.REQ_ID == req_id).order_by(PjtRcmdRslt.RCMD_RANK)
    return list(db.scalars(stmt))
