import uuid
from datetime import date

from sqlalchemy import select

from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.hr_skill_mst import HrSkillMst
from app.schemas.ai_chat import ParsedResourceQuery
from app.services.ai_resource_search import search_resources


def _create_employee(client, headers, dept, jikgup, *, jikmu_id=None) -> str:
    empl_no = f"PYTESTAI{uuid.uuid4().hex[:6]}"
    payload = {
        "EMPL_NO": empl_no,
        "EMPL_NM": "AI검색테스트",
        "EMAIL_ADDR": f"{empl_no}@example.com",
        "DEPT_ID": str(dept.DEPT_ID),
        "JIKGUP_ID": str(jikgup.JIKGUP_ID),
    }
    if jikmu_id is not None:
        payload["JIKMU_ID"] = str(jikmu_id)
    resp = client.post("/api/v1/employees", headers=headers, json=payload)
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def test_search_resources_matches_job_type(client, admin_token, db_session, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    developer = db_session.scalar(select(HrJikmuMst).where(HrJikmuMst.JIKMU_CD == "DEVELOPER"))
    empl_id = _create_employee(client, headers, dept, jikgup, jikmu_id=developer.JIKMU_ID)

    parsed = ParsedResourceQuery(intent="resource_search", job_type="DEVELOPER", confidence=0.5)
    result = search_resources(db_session, parsed)

    assert any(item.EMPL_ID == uuid.UUID(empl_id) for item in result.items)
    assert result.total == len(result.items)
    assert "명을 찾았습니다" in result.summary


def test_search_resources_no_match_returns_empty_summary(db_session):
    parsed = ParsedResourceQuery(intent="resource_search", department="존재하지않는부서", confidence=0.5)
    result = search_resources(db_session, parsed)

    assert result.total == 0
    assert result.items == []
    assert result.summary == "조건에 맞는 인력을 찾지 못했습니다."


def test_search_resources_filters_by_available_from(client, admin_token, db_session, dept, jikgup):
    """가동 가능일이 요청 시점보다 늦게 잡히는 사원은 결과에서 제외되어야 한다."""
    from app.models.pjt_asgn_his import PjtAsgnHis
    from app.models.pjt_mst import PjtMst

    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)

    project = PjtMst(
        PJT_ID=uuid.uuid4(),
        PJT_CD=f"PYTESTAI-{uuid.uuid4().hex[:8]}",
        PJT_NM="AI검색테스트프로젝트",
        PJT_STAT_CD="RUNNING",
        STRT_DT=date(2026, 1, 1),
    )
    db_session.add(project)
    db_session.flush()

    create_resp = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "EMPL_ID": empl_id,
            "PJT_ID": str(project.PJT_ID),
            "PRJT_ROLE_NM": "Backend",
            "ALLOC_RT": 100,
            "ASGN_STRT_DT": "2026-01-01",
            "ASGN_END_DT": "2026-12-31",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert create_resp.status_code == 201

    parsed = ParsedResourceQuery(
        intent="resource_search", available_from=date(2026, 2, 1), department=dept.DEPT_NM, confidence=0.5
    )
    result = search_resources(db_session, parsed)

    assert all(item.EMPL_ID != uuid.UUID(empl_id) for item in result.items)


def test_search_resources_skips_extra_skills(db_session):
    skills = list(db_session.scalars(select(HrSkillMst).limit(2)))
    parsed = ParsedResourceQuery(
        intent="resource_search",
        skills=[skills[0].SKILL_NM, skills[1].SKILL_NM],
        confidence=0.5,
    )
    result = search_resources(db_session, parsed)

    assert result.skipped_skills == [skills[1].SKILL_NM]
