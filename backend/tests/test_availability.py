import uuid
from datetime import date

from sqlalchemy import select

from app.models.hr_skill_mst import HrSkillMst
from app.models.pjt_mst import PjtMst


def _create_project(db_session) -> PjtMst:
    project = PjtMst(
        PJT_ID=uuid.uuid4(),
        PJT_CD=f"PYTEST-{uuid.uuid4().hex[:8]}",
        PJT_NM="테스트프로젝트",
        PJT_STAT_CD="RUNNING",
        STRT_DT=date(2026, 1, 1),
    )
    db_session.add(project)
    db_session.flush()
    return project


def _create_employee(client, headers, dept, jikgup) -> str:
    empl_no = f"PYTESTAVAIL{uuid.uuid4().hex[:6]}"
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "가동률테스트",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def test_availability_list_includes_available_employee(client, admin_token, dept, jikgup):
    """투입 이력이 전혀 없는 사원은 목록에서 AVAILABLE(즉시 가동)로 분류되어야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)

    resp = client.get("/api/v1/availability", headers=headers, params={"dept_id": str(dept.DEPT_ID)})
    assert resp.status_code == 200
    item = next((i for i in resp.json() if i["EMPL_ID"] == empl_id), None)
    assert item is not None
    assert item["AVAIL_STAT_CD"] == "AVAILABLE"
    assert item["TOT_ALLOC_RT"] == 0


def test_availability_list_reflects_partial_allocation(client, admin_token, db_session, dept, jikgup):
    """활성 투입(RUNNING, 50%)이 있는 사원은 PARTIAL로 분류되어야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)
    project = _create_project(db_session)

    create_resp = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "EMPL_ID": empl_id,
            "PJT_ID": str(project.PJT_ID),
            "PRJT_ROLE_NM": "Backend",
            "ALLOC_RT": 50,
            "ASGN_STRT_DT": "2026-01-01",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert create_resp.status_code == 201

    resp = client.get("/api/v1/availability", headers=headers, params={"dept_id": str(dept.DEPT_ID)})
    assert resp.status_code == 200
    item = next(i for i in resp.json() if i["EMPL_ID"] == empl_id)
    assert item["AVAIL_STAT_CD"] == "PARTIAL"
    assert item["TOT_ALLOC_RT"] == 50


def test_availability_list_filters_by_jikmu_id(client, admin_token, dept, jikgup):
    """직무 유형(jikmu_id)이 없는 사원은 해당 필터로 조회 시 제외되어야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)

    resp = client.get(
        "/api/v1/availability", headers=headers, params={"jikmu_id": str(uuid.uuid4())}
    )
    assert resp.status_code == 200
    assert all(i["EMPL_ID"] != empl_id for i in resp.json())


def test_availability_list_filters_by_skill_and_min_prfcy_levl(client, admin_token, db_session, dept, jikgup):
    """skill_id + min_prfcy_levl 필터는 해당 기술을 그 숙련도 이상으로 보유한 사원만 포함해야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    skilled_empl_id = _create_employee(client, headers, dept, jikgup)
    unskilled_empl_id = _create_employee(client, headers, dept, jikgup)
    skill = db_session.scalars(select(HrSkillMst).limit(1)).first()

    create_resp = client.post(
        "/api/v1/employee-skills",
        headers=headers,
        json={"EMPL_ID": skilled_empl_id, "SKILL_ID": str(skill.SKILL_ID), "PRFCY_LEVL": 4},
    )
    assert create_resp.status_code == 201

    resp = client.get(
        "/api/v1/availability",
        headers=headers,
        params={"dept_id": str(dept.DEPT_ID), "skill_id": str(skill.SKILL_ID), "min_prfcy_levl": 3},
    )
    assert resp.status_code == 200
    result_ids = {i["EMPL_ID"] for i in resp.json()}
    assert skilled_empl_id in result_ids
    assert unskilled_empl_id not in result_ids

    resp_higher_bar = client.get(
        "/api/v1/availability",
        headers=headers,
        params={"dept_id": str(dept.DEPT_ID), "skill_id": str(skill.SKILL_ID), "min_prfcy_levl": 5},
    )
    assert skilled_empl_id not in {i["EMPL_ID"] for i in resp_higher_bar.json()}


def test_viewer_cannot_view_availability_list(client, viewer_token):
    """SCR-010 접근 권한은 "A H P T E"로 VIEWER를 제외한다(설계서 기준, PERM_JSON에도 반영됨)."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/availability", headers=headers)

    assert resp.status_code == 403
