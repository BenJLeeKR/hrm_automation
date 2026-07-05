import uuid
from datetime import date

from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst


def test_weekly_report_default(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/reports/weekly", headers=headers)

    assert resp.status_code == 200
    body = resp.json()
    assert "dept_utilization" in body
    assert "skill_distribution" in body


def test_weekly_report_reflects_new_employee(client, admin_token, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    before = client.get("/api/v1/reports/weekly", headers=headers, params={"week": "2026-W27"}).json()

    create_resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": "PYTESTRPT001",
            "EMPL_NM": "리포트테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert create_resp.status_code == 201

    after = client.get("/api/v1/reports/weekly", headers=headers, params={"week": "2026-W27"}).json()
    assert after["total_active_employees"] == before["total_active_employees"] + 1
    assert after["available_count"] == before["available_count"] + 1


def test_weekly_report_invalid_week_returns_422(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/reports/weekly", headers=headers, params={"week": "invalid"})

    assert resp.status_code == 422


def test_monthly_report_invalid_month_returns_422(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/reports/monthly", headers=headers, params={"month": "abc"})

    assert resp.status_code == 422


def test_monthly_report_default(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/reports/monthly", headers=headers)

    assert resp.status_code == 200


def test_viewer_cannot_view_reports(client, viewer_token):
    """설계서(SCR-013) 접근 권한이 A H P E이며 VIEWER는 제외되어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/reports/weekly", headers=headers)

    assert resp.status_code == 403


def test_send_weekly_report_without_webhook_returns_sent_false(client, admin_token, monkeypatch):
    """`TEAMS_WEBHOOK_URL` 미설정(로컬/테스트 기본값)이면 예외 없이 sent=False로
    안내한다 — `PJT_ASGN_END_ALERT` 배치와 동일한 선택적 연동 원칙(§9-1)."""
    from app.core.config import settings

    monkeypatch.setattr(settings, "TEAMS_WEBHOOK_URL", "")
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/reports/send", headers=headers, json={"report_type": "weekly", "period": "2026-W27"}
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["sent"] is False
    assert "TEAMS_WEBHOOK_URL" in body["message"]


def test_send_monthly_report_with_webhook_calls_teams(client, admin_token, monkeypatch):
    """`TEAMS_WEBHOOK_URL`이 설정된 경우를 실제 네트워크 호출 없이 모킹해 검증한다."""
    from app.core.config import settings

    monkeypatch.setattr(settings, "TEAMS_WEBHOOK_URL", "https://example.invalid/webhook")
    monkeypatch.setattr("app.api.v1.reports.send_teams_message", lambda text: True)
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/reports/send", headers=headers, json={"report_type": "monthly", "period": "202607"}
    )

    assert resp.status_code == 200
    assert resp.json()["sent"] is True


def test_send_report_invalid_period_returns_422(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/reports/send", headers=headers, json={"report_type": "weekly", "period": "invalid"}
    )

    assert resp.status_code == 422


def test_viewer_cannot_send_report(client, viewer_token):
    """`reports.admin` 권한이 없는 VIEWER는 발송 API도 차단되어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.post(
        "/api/v1/reports/send", headers=headers, json={"report_type": "weekly", "period": "2026-W27"}
    )

    assert resp.status_code == 403


def test_utilization_matrix_reflects_assignment(client, admin_token, db_session, dept, jikgup):
    """월별 가동률 통계 매트릭스가 실제 투입 이력을 반영해야 한다(SCR-013 탭 3)."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": f"PYTESTMTX{uuid.uuid4().hex[:6]}",
            "EMPL_NM": "매트릭스테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert empl_resp.status_code == 201
    empl_id = empl_resp.json()["EMPL_ID"]

    project = PjtMst(
        PJT_ID=uuid.uuid4(),
        PJT_CD=f"PYTESTMTX-{uuid.uuid4().hex[:8]}",
        PJT_NM="매트릭스테스트프로젝트",
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
            "ALLOC_RT": 60,
            "ASGN_STRT_DT": "2026-01-01",
            "ASGN_END_DT": "2026-02-28",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert create_resp.status_code == 201

    resp = client.get(
        "/api/v1/reports/utilization-matrix",
        headers=headers,
        params={"from": "202601", "to": "202603", "dept_id": str(dept.DEPT_ID)},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["period"] == ["2026-01", "2026-02", "2026-03"]

    row = next(e for e in body["employees"] if e["empl_no"] == empl_resp.json()["EMPL_NO"])
    assert row["subtotal"] == [60, 60, 0]
    assert row["rows"][0]["pjt_nm"] == "매트릭스테스트프로젝트"
    assert row["over_100_months"] == []


def test_utilization_matrix_flags_over_100_percent(client, admin_token, db_session, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": f"PYTESTMTX{uuid.uuid4().hex[:6]}",
            "EMPL_NM": "초과테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    empl_id = empl_resp.json()["EMPL_ID"]

    projects = []
    for i in range(2):
        project = PjtMst(
            PJT_ID=uuid.uuid4(),
            PJT_CD=f"PYTESTMTX-{uuid.uuid4().hex[:8]}",
            PJT_NM=f"초과테스트프로젝트{i}",
            PJT_STAT_CD="RUNNING",
            STRT_DT=date(2026, 1, 1),
        )
        db_session.add(project)
        projects.append(project)
    db_session.flush()

    # 첫 건은 정상 API로 등록(100% 이내), 두 번째 건은 API의 100% 초과 검증(409)을 우회해
    # DB에 직접 넣는다 — 매트릭스의 "100% 초과 경고"는 정상 흐름에서는 발생할 수 없는
    # 레거시/이관 데이터의 정합성 위반을 잡아내기 위한 기능이라, 그 상황을 재현해야 한다.
    resp = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "EMPL_ID": empl_id,
            "PJT_ID": str(projects[0].PJT_ID),
            "PRJT_ROLE_NM": "Backend",
            "ALLOC_RT": 70,
            "ASGN_STRT_DT": "2026-01-01",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert resp.status_code == 201

    db_session.add(
        PjtAsgnHis(
            EMPL_ID=uuid.UUID(empl_id),
            PJT_ID=projects[1].PJT_ID,
            ASGN_TYPE_CD="RUNNING",
            PRJT_ROLE_NM="Backend",
            ALLOC_RT=70,
            ASGN_STRT_DT=date(2026, 1, 1),
            ASGN_STAT_CD="ACTIVE",
        )
    )
    db_session.flush()

    resp = client.get(
        "/api/v1/reports/utilization-matrix",
        headers=headers,
        params={"from": "202601", "to": "202601", "dept_id": str(dept.DEPT_ID)},
    )
    assert resp.status_code == 200
    row = next(e for e in resp.json()["employees"] if e["empl_no"] == empl_resp.json()["EMPL_NO"])
    assert row["subtotal"] == [140]
    assert row["over_100_months"] == ["2026-01"]


def test_utilization_matrix_invalid_range_returns_422(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get(
        "/api/v1/reports/utilization-matrix", headers=headers, params={"from": "202612", "to": "202601"}
    )

    assert resp.status_code == 422
