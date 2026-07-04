import uuid
from datetime import date, timedelta

from app.models.hr_dept_mst import HrDeptMst
from app.services.ai_parser import parse_query


def _first_of_month(base: date, *, offset_months: int) -> date:
    total = base.month - 1 + offset_months
    year = base.year + total // 12
    month = total % 12 + 1
    return date(year, month, 1)


def test_parses_job_type_and_skill_with_next_month(db_session):
    result = parse_query(db_session, "다음 달 투입 가능한 Java 아키텍트 추천해줘")
    assert result.job_type == "ARCHITECT"
    assert "Java" in result.skills
    assert result.available_from == _first_of_month(date.today(), offset_months=1)
    assert result.intent == "resource_search"


def test_parses_specific_month_and_partial_skill_name(db_session):
    result = parse_query(db_session, "8월에 가능한 Spring 개발자 찾아줘")
    assert result.job_type == "DEVELOPER"
    assert "Spring Boot" in result.skills
    today = date.today()
    expected_year = today.year if 8 >= today.month else today.year + 1
    assert result.available_from == date(expected_year, 8, 1)


def test_parses_department_and_skill(db_session):
    dept = HrDeptMst(DEPT_ID=uuid.uuid4(), DEPT_CD=f"PYTESTAI-{uuid.uuid4().hex[:8]}", DEPT_NM="개발1팀")
    db_session.add(dept)
    db_session.flush()

    result = parse_query(db_session, "개발1팀에서 Python 가능한 사람 있어?")
    assert result.department == "개발1팀"
    assert "Python" in result.skills


def test_parses_this_month_end_of_assignment_phrase(db_session):
    result = parse_query(db_session, "이번 달 종료 예정자 알려줘")
    assert result.available_from == _first_of_month(date.today(), offset_months=0)


def test_parses_job_type_and_flags_unresolved_threshold(db_session):
    result = parse_query(db_session, "가동률 50% 이하인 PM 찾아줘")
    assert result.job_type == "PM"
    assert any("가동률" in term for term in result.unresolved_terms)
    assert "PM" not in result.unresolved_terms


def test_flags_unmatched_acronym_as_unresolved(db_session):
    result = parse_query(db_session, "K-ICS 경험 있는 BA 찾아줘")
    assert result.job_type == "BA"
    assert "K-ICS" in result.unresolved_terms


def test_parses_db_skill_with_job_type(db_session):
    result = parse_query(db_session, "PostgreSQL 가능한 백엔드 개발자")
    assert result.job_type == "DEVELOPER"
    assert "PostgreSQL" in result.skills


def test_parses_today_availability_and_flags_seniority_keyword(db_session):
    result = parse_query(db_session, "즉시 투입 가능한 시니어 개발자")
    assert result.available_from == date.today()
    assert result.job_type == "DEVELOPER"
    assert "시니어" in result.unresolved_terms


def test_parses_next_week_and_partial_skill(db_session):
    result = parse_query(db_session, "다음 주부터 가능한 React 개발자")
    today = date.today()
    assert result.available_from == today + timedelta(days=7 - today.weekday())
    assert "React" in result.skills


def test_parses_job_type_and_business_skill_keyword(db_session):
    result = parse_query(db_session, "보험 프로젝트 경험 있는 아키텍트")
    assert result.job_type == "ARCHITECT"
    assert "보험업무" in result.skills


def test_parses_min_proficiency_level(db_session):
    result = parse_query(db_session, "숙련도 3 이상인 Java 개발자 찾아줘")
    assert result.min_proficiency_level == 3
    assert "Java" in result.skills
    assert result.job_type == "DEVELOPER"


def test_unresolvable_query_returns_unknown_intent(db_session):
    result = parse_query(db_session, "안녕하세요 반갑습니다")
    assert result.intent == "unknown"
    assert result.job_type is None
    assert result.skills == []
