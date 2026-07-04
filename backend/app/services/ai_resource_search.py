from datetime import date

from sqlalchemy.orm import Session

from app.repositories.codes import list_departments, list_job_types
from app.repositories.hr_avail_snap import list_availability
from app.repositories.hr_empl_mst import list_employees_by_ids
from app.repositories.hr_skill_mst import list_skills
from app.schemas.ai_chat import ParsedResourceQuery, ResourceSearchItem, ResourceSearchResult

# 파싱 결과 → SQL 조회 → 결과 요약 흐름 (로드맵 §8 후속 작업, `ai_parser.py`의 뒷단).
#
# whitelist 원칙(사용자 지침, 이전 작업에서 확정): LLM이 SQL을 생성하지 않는다 — 이 모듈은
# `ParsedResourceQuery.intent == "resource_search"`인 경우에만 기존 repository
# (`hr_avail_snap.list_availability` 등, §8 "직무 유형·기술·숙련도 복합 필터 검색 API
# 구현"에서 이미 만든 함수)를 그대로 호출해 검색하고, 그 외 intent(예: "unknown")는 이
# 모듈을 아예 호출하지 않는다(`app/api/v1/ai_chat.py`에서 분기).
#
# 알려진 제약: `list_availability`는 `skill_id` 파라미터 하나만 지원해 기술 조건 1개까지만
# DB 조회에 반영할 수 있다. 파싱된 기술이 여러 개면 첫 번째만 조회에 사용하고 나머지는
# `skipped_skills`로 반환해, 호출부(요약 문구)가 사용자에게 "일부 조건은 반영되지 않았다"고
# 알릴 수 있게 한다(다중 기술 AND 조건 조회는 필요 시 별도 후속 작업으로 확장).


def _resolve_jikmu_id(db: Session, job_type_cd: str | None):
    if job_type_cd is None:
        return None
    for jt in list_job_types(db):
        if jt.JIKMU_CD == job_type_cd:
            return jt.JIKMU_ID
    return None


def _resolve_dept_id(db: Session, department_name: str | None):
    if department_name is None:
        return None
    for dept in list_departments(db):
        if dept.DEPT_NM == department_name:
            return dept.DEPT_ID
    return None


def _resolve_skill_id(db: Session, skill_name: str | None):
    if skill_name is None:
        return None
    for skill in list_skills(db):
        if skill.SKILL_NM == skill_name:
            return skill.SKILL_ID
    return None


def _build_summary(items: list[ResourceSearchItem], *, skipped_skills: list[str]) -> str:
    if not items:
        return "조건에 맞는 인력을 찾지 못했습니다."

    preview = ", ".join(f"{i.EMPL_NM}({i.EMPL_NO}, 가동률 {i.AVAIL_RT}%)" for i in items[:5])
    remaining = len(items) - 5
    summary = f"조건에 맞는 인력 {len(items)}명을 찾았습니다: {preview}"
    if remaining > 0:
        summary += f" 외 {remaining}명"
    if skipped_skills:
        summary += f" (참고: '{', '.join(skipped_skills)}' 조건은 이번 검색에 반영되지 않았습니다)"
    return summary


def search_resources(db: Session, parsed: ParsedResourceQuery, *, today: date | None = None) -> ResourceSearchResult:
    """`intent == "resource_search"`로 파싱된 조건을 기존 가동률 조회 repository로 검색한다.

    SQL은 여기서 새로 작성하지 않고 `list_availability`(§8 "직무 유형·기술·숙련도 복합
    필터 검색 API 구현"에서 구현한 기존 함수)를 그대로 재사용한다.
    """
    today = today or date.today()

    jikmu_id = _resolve_jikmu_id(db, parsed.job_type)
    dept_id = _resolve_dept_id(db, parsed.department)
    skill_id = _resolve_skill_id(db, parsed.skills[0]) if parsed.skills else None
    skipped_skills = parsed.skills[1:] if len(parsed.skills) > 1 else []

    # 조건은 있었는데 마스터 데이터에서 ID로 변환하지 못한 경우(예: 삭제된 부서명, 오타)
    # 필터를 조용히 무시하고 전체 조회로 흘려보내면 안 된다 — 해당 조건은 만족할 수 없으므로
    # 즉시 빈 결과로 반환한다. (`ai_parser.py`가 실제 마스터 데이터로만 값을 채우므로
    # `/ai/chat` 정상 흐름에서는 거의 발생하지 않지만, 이 함수를 직접 호출하는 경우까지
    # 방어한다.)
    if (parsed.job_type and jikmu_id is None) or (parsed.department and dept_id is None):
        return ResourceSearchResult(total=0, items=[], summary="조건에 맞는 인력을 찾지 못했습니다.", skipped_skills=[])
    if parsed.skills and skill_id is None:
        return ResourceSearchResult(total=0, items=[], summary="조건에 맞는 인력을 찾지 못했습니다.", skipped_skills=[])

    results = list_availability(
        db,
        snap_dt=today,
        jikmu_id=jikmu_id,
        dept_id=dept_id,
        skill_id=skill_id,
        min_prfcy_levl=parsed.min_proficiency_level,
    )

    if parsed.available_from is not None:
        results = [
            r
            for r in results
            if r.AVAIL_STAT_CD == "AVAILABLE"
            or (r.AVAIL_STRT_DT is not None and r.AVAIL_STRT_DT <= parsed.available_from)
        ]

    employees_by_id = {e.EMPL_ID: e for e in list_employees_by_ids(db, [r.EMPL_ID for r in results])}
    items = [
        ResourceSearchItem(
            EMPL_ID=r.EMPL_ID,
            EMPL_NO=employees_by_id[r.EMPL_ID].EMPL_NO,
            EMPL_NM=employees_by_id[r.EMPL_ID].EMPL_NM,
            AVAIL_STAT_CD=r.AVAIL_STAT_CD,
            AVAIL_RT=r.AVAIL_RT,
            AVAIL_STRT_DT=r.AVAIL_STRT_DT,
        )
        for r in results
        if r.EMPL_ID in employees_by_id
    ]

    return ResourceSearchResult(
        total=len(items),
        items=items,
        summary=_build_summary(items, skipped_skills=skipped_skills),
        skipped_skills=skipped_skills,
    )
