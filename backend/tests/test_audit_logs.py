def test_list_audit_logs_default(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/audit-logs", headers=headers)

    assert resp.status_code == 200
    body = resp.json()
    assert "items" in body and "total" in body
    # 로그인 자체가 감사 로그(ACT_CD='LOGIN')로 기록되므로 최소 1건은 항상 존재해야 한다
    assert body["total"] >= 1


def test_list_audit_logs_filters_by_act_cd(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/audit-logs", headers=headers, params={"act_cd": "LOGIN"})

    assert resp.status_code == 200
    assert all(item["ACT_CD"] == "LOGIN" for item in resp.json()["items"])


def test_list_audit_logs_filters_by_user_lgid(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/audit-logs", headers=headers, params={"user_lgid": "nonexistent-user-xyz"})

    assert resp.status_code == 200
    assert resp.json()["items"] == []


def test_viewer_cannot_view_audit_logs(client, viewer_token):
    """설계서(SCR-016) 접근 권한이 "A(Admin 전용)"이므로 VIEWER는 403이어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/audit-logs", headers=headers)

    assert resp.status_code == 403
