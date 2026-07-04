import re
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.hr_skill_mst import HrSkillMst
from app.repositories.codes import list_departments, list_job_types
from app.repositories.hr_skill_mst import list_skills
from app.schemas.ai_chat import ParsedResourceQuery

# 자연어 조건 파싱 (로드맵 §8 "자연어 조건 파싱 구현", Phase 6 후속 작업 — 사용자 확정에 따라
# AI Chat 1차 구현 범위(LLM 단순 호출/응답, `app/services/ai_chat.py`)와 분리된 별도 모듈이다.
#
# 이번 작업 범위는 파싱까지만이다:
# - LLM에 임의 SQL을 생성시키지 않는다 — 규칙 기반(마스터 데이터 매칭 + 정규식)으로만 파싱한다.
# - 실제 DB 조회(리소스 검색)는 수행하지 않는다 — 마스터 데이터 매칭을 위한 조회(직무 유형/
#   기술/부서 목록)만 기존 repository(`codes.py`, `hr_skill_mst.py`)를 재사용해 수행한다.
# - 파싱 결과를 SQL 조회에 연결하는 것은 후속 작업("파싱 결과 → SQL 조회 → 결과 요약 흐름
#   구현")에서 다루며, 그 작업 역시 LLM이 아닌 whitelist 기반 intent(`resource_search`)와
#   기존 repository/query builder를 통해서만 구현해야 한다(free-form SQL 생성·실행 금지).
# - 권한 필터링·환각 방지 프롬프트는 이번 작업에서 적용하지 않는다 — 이 함수는 순수 파싱만
#   담당하도록 `app/api/v1/ai_chat.py`(LLM 호출)와 독립된 모듈로 분리해, 후속 작업에서 권한
#   필터링 레이어를 이 함수의 호출부(파싱 결과를 SQL 조회에 넘기는 지점)에 끼워 넣을 수 있게
#   경계를 나눠뒀다.

_UNRESOLVED_KEYWORDS = ["시니어", "주니어", "책임급", "수석", "리드급"]
_THRESHOLD_PATTERN = re.compile(r"가동률\s*\d+\s*%\s*(이상|이하|미만|초과)")
_PROFICIENCY_PATTERN = re.compile(r"숙련도\s*(\d)\s*(?:점)?\s*이상")
_ACRONYM_PATTERN = re.compile(r"\b[A-Z][A-Z0-9\-]{1,10}\b")


def _first_of_month(base: date, *, offset_months: int) -> date:
    total = base.month - 1 + offset_months
    year = base.year + total // 12
    month = total % 12 + 1
    return date(year, month, 1)


def _resolve_available_from(message: str, today: date) -> date | None:
    """가동일/기간 표현("오늘"/"이번 달"/"다음 달"/특정 월/특정 날짜)을 날짜로 변환한다.

    "종료 예정"은 전용 필드가 없어, "해당 기간에 새로 가동 가능해지는 인력"이라는
    의미로 해석해 이번 달 1일로 근사한다(운영팀 확인 필요 시 §9 리스크로 별도 기록).
    """
    iso_match = re.search(r"(20\d{2})-(\d{1,2})-(\d{1,2})", message)
    if iso_match:
        year, month, day = (int(v) for v in iso_match.groups())
        try:
            return date(year, month, day)
        except ValueError:
            pass

    md_match = re.search(r"(\d{1,2})\s*월\s*(\d{1,2})\s*일", message)
    if md_match:
        month, day = (int(v) for v in md_match.groups())
        year = today.year if month >= today.month else today.year + 1
        try:
            return date(year, month, day)
        except ValueError:
            pass

    if "즉시" in message or "오늘" in message:
        return today
    if "다음달" in message or "다음 달" in message:
        return _first_of_month(today, offset_months=1)
    if "다음주" in message or "다음 주" in message:
        return today + timedelta(days=7 - today.weekday())
    if "이번달" in message or "이번 달" in message or "종료 예정" in message or "종료예정" in message:
        return _first_of_month(today, offset_months=0)

    month_only = re.search(r"(\d{1,2})\s*월(?!\s*\d)", message)
    if month_only:
        month = int(month_only.group(1))
        year = today.year if month >= today.month else today.year + 1
        return date(year, month, 1)

    return None


def _match_job_type(message: str, job_types: list[HrJikmuMst]) -> str | None:
    """직무 유형 매칭 — `JIKMU_CD`, `JIKMU_NM`, `JIKMU_NM`에서 부기 코드("(AA)" 등)를
    제거한 순수 명칭 3가지를 후보로 두고, 가장 긴(구체적인) 후보부터 일치를 확인한다."""
    candidates: list[tuple[str, str]] = []
    for jt in job_types:
        candidates.append((jt.JIKMU_NM, jt.JIKMU_CD))
        stripped = re.sub(r"\(.*?\)\s*$", "", jt.JIKMU_NM).strip()
        if stripped and stripped != jt.JIKMU_NM:
            candidates.append((stripped, jt.JIKMU_CD))
        candidates.append((jt.JIKMU_CD, jt.JIKMU_CD))
    candidates.sort(key=lambda c: len(c[0]), reverse=True)

    for text, code in candidates:
        if not text:
            continue
        if text.isascii() and text.isalnum():
            if re.search(rf"\b{re.escape(text)}\b", message, re.IGNORECASE):
                return code
        elif text in message:
            return code
    return None


def _match_skills(message: str, skills_master: list[HrSkillMst]) -> list[str]:
    """기술 매칭 — ① 기술명 전체가 문장에 그대로 포함된 경우를 우선 확인하고,
    ② "Spring 개발자"처럼 기술명 일부(토큰) 단위로만 언급된 경우를 보조로 매칭한다."""
    matched_names: list[str] = []
    matched_ids: set = set()
    lowered_message = message.lower()

    for skill in skills_master:
        if skill.SKILL_NM.lower() in lowered_message:
            matched_names.append(skill.SKILL_NM)
            matched_ids.add(skill.SKILL_ID)

    tokens = [t for t in re.split(r"[\s,]+", message) if len(t) >= 2]
    for token in tokens:
        # 영문 2글자 토큰(PM/BA/QA 등 직무 코드와 겹치기 쉬움)은 부분 일치 오탐 위험이 커
        # 기술 매칭 대상에서 제외한다 — 한글 2글자 단어("보험" 등)는 그대로 허용한다.
        if token.isascii() and len(token) < 3:
            continue
        lowered_token = token.lower()
        for skill in skills_master:
            if skill.SKILL_ID in matched_ids:
                continue
            if lowered_token in skill.SKILL_NM.lower():
                matched_names.append(skill.SKILL_NM)
                matched_ids.add(skill.SKILL_ID)
                break

    return matched_names


def _match_department(message: str, departments: list[HrDeptMst]) -> str | None:
    for dept in sorted(departments, key=lambda d: len(d.DEPT_NM), reverse=True):
        if dept.DEPT_NM in message:
            return dept.DEPT_NM
    return None


def _match_min_proficiency(message: str) -> int | None:
    match = _PROFICIENCY_PATTERN.search(message)
    if not match:
        return None
    level = int(match.group(1))
    return level if 1 <= level <= 5 else None


def _collect_unresolved_terms(message: str, *, job_type: str | None) -> list[str]:
    """표준 필드로 표현할 수 없는 조건(가동률 임계값, 연차/직급 뉘앙스, 매칭 실패한
    영문 약어 등)을 그대로 기록해, 후속 SQL 조회 단계나 사용자 재질의에 활용할 수 있게 한다."""
    unresolved: list[str] = []

    threshold_match = _THRESHOLD_PATTERN.search(message)
    if threshold_match:
        unresolved.append(threshold_match.group())

    for keyword in _UNRESOLVED_KEYWORDS:
        if keyword in message and keyword not in unresolved:
            unresolved.append(keyword)

    for token in _ACRONYM_PATTERN.findall(message):
        if token == job_type:
            continue
        if token not in unresolved:
            unresolved.append(token)

    return unresolved


def parse_query(db: Session, message: str) -> ParsedResourceQuery:
    """자연어 질의를 `ParsedResourceQuery` 표준 형태로 파싱한다 (SQL 조회는 수행하지 않음)."""
    today = date.today()

    job_type = _match_job_type(message, list_job_types(db))
    skills = _match_skills(message, list_skills(db))
    department = _match_department(message, list_departments(db))
    available_from = _resolve_available_from(message, today)
    min_proficiency_level = _match_min_proficiency(message)
    unresolved_terms = _collect_unresolved_terms(message, job_type=job_type)

    matched_count = sum(bool(v) for v in (job_type, skills, department, available_from, min_proficiency_level))
    if matched_count == 0:
        intent = "unknown"
        confidence = 0.2
    else:
        intent = "resource_search"
        confidence = min(0.95, 0.35 + 0.15 * matched_count)
    if unresolved_terms:
        confidence = max(0.1, confidence - 0.05 * len(unresolved_terms))

    return ParsedResourceQuery(
        intent=intent,
        job_type=job_type,
        skills=skills,
        min_proficiency_level=min_proficiency_level,
        available_from=available_from,
        department=department,
        confidence=round(confidence, 2),
        unresolved_terms=unresolved_terms,
    )
