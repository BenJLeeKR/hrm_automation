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
