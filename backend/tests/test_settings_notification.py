def test_get_notification_settings_masks_secret(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/settings/notification", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["smtp_password"] == ""


def test_update_and_get_notification_settings(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    put_resp = client.put(
        "/api/v1/settings/notification",
        headers=headers,
        json={
            "teams_webhook_url": "https://outlook.office.com/webhook/pytest",
            "smtp_host": "smtp.pytest.local",
            "smtp_port": "587",
            "smtp_user": "pytest-user",
            "smtp_password": "pytest-secret",
            "email_from": "pytest@example.com",
        },
    )
    assert put_resp.status_code == 200
    body = put_resp.json()
    assert body["teams_webhook_url"] == "https://outlook.office.com/webhook/pytest"
    assert body["smtp_password"] == "*****"

    get_resp = client.get("/api/v1/settings/notification", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["smtp_host"] == "smtp.pytest.local"


def test_update_blank_password_keeps_existing_value(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    client.put(
        "/api/v1/settings/notification",
        headers=headers,
        json={"smtp_password": "keep-me-secret"},
    )
    resp = client.put(
        "/api/v1/settings/notification",
        headers=headers,
        json={"smtp_host": "smtp.other.local"},
    )
    assert resp.status_code == 200
    assert resp.json()["smtp_password"] == "*****"
    assert resp.json()["smtp_host"] == "smtp.other.local"


def test_test_notification_channel_unset_teams(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/settings/notification/test", headers=headers, json={"channel": "teams"}
    )
    assert resp.status_code == 200
    assert resp.json()["sent"] is False


def test_test_notification_channel_incomplete_smtp(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/settings/notification/test", headers=headers, json={"channel": "email"}
    )
    assert resp.status_code == 200
    assert resp.json()["sent"] is False


def test_viewer_forbidden(client, viewer_token):
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/settings/notification", headers=headers)
    assert resp.status_code == 403
