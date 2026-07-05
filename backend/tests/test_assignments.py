import uuid
from datetime import date

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
    empl_no = f"PYTESTASGN{uuid.uuid4().hex[:6]}"
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "투입테스트",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def _assignment_payload(empl_id: str, pjt_id: str, alloc_rt: int, role: str) -> dict:
    return {
        "EMPL_ID": empl_id,
        "PJT_ID": pjt_id,
        "PRJT_ROLE_NM": role,
        "ALLOC_RT": alloc_rt,
        "ASGN_STRT_DT": "2026-01-01",
        "ASGN_STAT_CD": "ACTIVE",
        "ASGN_TYPE_CD": "RUNNING",
    }


def test_alloc_rt_over_100_percent_rejected(client, db_session, admin_token, dept, jikgup):
    """동일 사원·겹치는 기간의 ALLOC_RT 합계가 100%를 초과하면 409여야 한다 (ERD §3.9)."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    project = _create_project(db_session)
    empl_id = _create_employee(client, headers, dept, jikgup)

    first = client.post("/api/v1/assignments", headers=headers, json=_assignment_payload(empl_id, str(project.PJT_ID), 60, "개발"))
    assert first.status_code == 201

    second = client.post("/api/v1/assignments", headers=headers, json=_assignment_payload(empl_id, str(project.PJT_ID), 50, "QA"))
    assert second.status_code == 409


def test_alloc_rt_exactly_100_percent_allowed(client, db_session, admin_token, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    project = _create_project(db_session)
    empl_id = _create_employee(client, headers, dept, jikgup)

    first = client.post("/api/v1/assignments", headers=headers, json=_assignment_payload(empl_id, str(project.PJT_ID), 60, "개발"))
    assert first.status_code == 201

    second = client.post("/api/v1/assignments", headers=headers, json=_assignment_payload(empl_id, str(project.PJT_ID), 40, "QA"))
    assert second.status_code == 201


def test_cancelled_assignment_excluded_from_alloc_rt_check(client, db_session, admin_token, dept, jikgup):
    """CANCELED 상태로 전환된 투입은 100% 합계 집계에서 제외되어야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    project = _create_project(db_session)
    empl_id = _create_employee(client, headers, dept, jikgup)

    first = client.post("/api/v1/assignments", headers=headers, json=_assignment_payload(empl_id, str(project.PJT_ID), 60, "개발"))
    assert first.status_code == 201
    asgn_id = first.json()["ASGN_ID"]

    cancel_resp = client.patch(f"/api/v1/assignments/{asgn_id}", headers=headers, json={"ASGN_STAT_CD": "CANCELED"})
    assert cancel_resp.status_code == 200

    second = client.post("/api/v1/assignments", headers=headers, json=_assignment_payload(empl_id, str(project.PJT_ID), 80, "QA"))
    assert second.status_code == 201
