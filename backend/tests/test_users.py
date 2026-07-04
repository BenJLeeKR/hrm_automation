import uuid


def test_create_and_list_users(client, admin_token, admin_role):
    headers = {"Authorization": f"Bearer {admin_token}"}
    login_id = f"pytest_{uuid.uuid4().hex[:8]}"

    create_resp = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "USER_LGID": login_id,
            "EMAIL_ADDR": f"{login_id}@example.com",
            "password": "Str0ng!Pass",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )
    assert create_resp.status_code == 201
    assert "password" not in create_resp.json()
    assert "ENCR_PWD" not in create_resp.json()

    list_resp = client.get("/api/v1/users", headers=headers)
    assert list_resp.status_code == 200
    assert any(u["USER_LGID"] == login_id for u in list_resp.json())


def test_weak_password_rejected(client, admin_token, admin_role):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "USER_LGID": f"pytest_{uuid.uuid4().hex[:8]}",
            "EMAIL_ADDR": "weak@example.com",
            "password": "weak",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )
    assert resp.status_code == 422


def test_duplicate_login_id_returns_409(client, admin_token, admin_role):
    headers = {"Authorization": f"Bearer {admin_token}"}
    login_id = f"pytest_{uuid.uuid4().hex[:8]}"
    payload = {
        "USER_LGID": login_id,
        "EMAIL_ADDR": f"{login_id}@example.com",
        "password": "Str0ng!Pass",
        "ROLE_ID": str(admin_role.ROLE_ID),
    }

    first = client.post("/api/v1/users", headers=headers, json=payload)
    assert first.status_code == 201

    payload["EMAIL_ADDR"] = f"{login_id}-other@example.com"
    second = client.post("/api/v1/users", headers=headers, json=payload)
    assert second.status_code == 409


def test_viewer_cannot_manage_users(client, viewer_token, admin_role):
    """설계서(SCR-015) 접근 권한이 "A(Admin 전용)"이므로 VIEWER는 조회·등록 모두 403이어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}

    list_resp = client.get("/api/v1/users", headers=headers)
    assert list_resp.status_code == 403

    create_resp = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "USER_LGID": f"pytest_{uuid.uuid4().hex[:8]}",
            "EMAIL_ADDR": "viewer-try@example.com",
            "password": "Str0ng!Pass",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )
    assert create_resp.status_code == 403
