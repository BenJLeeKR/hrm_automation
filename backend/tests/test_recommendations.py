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
    empl_no = f"PYTESTRCMD{uuid.uuid4().hex[:6]}"
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "추천테스트",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def test_create_resource_request(client, admin_token, db_session):
    headers = {"Authorization": f"Bearer {admin_token}"}
    project = _create_project(db_session)

    resp = client.post(
        "/api/v1/resource-requests",
        headers=headers,
        json={
            "PJT_ID": str(project.PJT_ID),
            "REQ_ROLE_NM": "Backend",
            "MIN_ALLOC_RT": 50,
            "REQ_AVAIL_DT": "2026-08-01",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["REQ_STAT_CD"] == "OPEN"


def test_score_and_retrieve_recommendation(client, admin_token, db_session, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    project = _create_project(db_session)
    empl_id = _create_employee(client, headers, dept, jikgup)

    req_resp = client.post(
        "/api/v1/resource-requests",
        headers=headers,
        json={
            "PJT_ID": str(project.PJT_ID),
            "REQ_ROLE_NM": "Backend",
            "MIN_ALLOC_RT": 50,
            "REQ_AVAIL_DT": "2026-08-01",
        },
    )
    req_id = req_resp.json()["REQ_ID"]

    score_resp = client.post(
        "/api/v1/recommendations/score", headers=headers, json={"req_id": req_id}
    )
    assert score_resp.status_code == 200
    results = score_resp.json()
    assert any(r["EMPL_ID"] == empl_id for r in results)
    # 투입 이력이 없는 사원은 즉시 가동 가능해 가동일 조건(15점)을 항상 충족해야 한다
    candidate = next(r for r in results if r["EMPL_ID"] == empl_id)
    assert candidate["SCORE_DTL_JSON"]["availability"] == 15
    assert candidate["RCMD_RANK"] == 1

    get_resp = client.get(f"/api/v1/recommendations/{req_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json() == results


def test_score_rerun_replaces_previous_results(client, admin_token, db_session, dept, jikgup):
    """동일 요청으로 추천을 재실행하면 이전 결과가 남지 않고 최신 결과로 교체되어야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    project = _create_project(db_session)
    _create_employee(client, headers, dept, jikgup)

    req_resp = client.post(
        "/api/v1/resource-requests",
        headers=headers,
        json={
            "PJT_ID": str(project.PJT_ID),
            "REQ_ROLE_NM": "Backend",
            "MIN_ALLOC_RT": 50,
            "REQ_AVAIL_DT": "2026-08-01",
        },
    )
    req_id = req_resp.json()["REQ_ID"]

    first = client.post("/api/v1/recommendations/score", headers=headers, json={"req_id": req_id})
    second = client.post("/api/v1/recommendations/score", headers=headers, json={"req_id": req_id})

    final = client.get(f"/api/v1/recommendations/{req_id}", headers=headers)
    assert len(final.json()) == len(second.json()) == len(first.json())


def test_score_nonexistent_request_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/recommendations/score", headers=headers, json={"req_id": str(uuid.uuid4())}
    )

    assert resp.status_code == 404


def test_viewer_cannot_create_resource_request(client, viewer_token, db_session):
    """VIEWER는 PERM_JSON상 recommendations.create 권한이 없어 403이어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    project = _create_project(db_session)

    resp = client.post(
        "/api/v1/resource-requests",
        headers=headers,
        json={
            "PJT_ID": str(project.PJT_ID),
            "REQ_ROLE_NM": "Backend",
            "MIN_ALLOC_RT": 50,
            "REQ_AVAIL_DT": "2026-08-01",
        },
    )

    assert resp.status_code == 403
