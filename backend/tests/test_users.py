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


def test_patch_user_updates_role_and_email(client, admin_token, admin_role, viewer_role):
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
    user_id = create_resp.json()["USER_ID"]

    patch_resp = client.patch(
        f"/api/v1/users/{user_id}",
        headers=headers,
        json={"ROLE_ID": str(viewer_role.ROLE_ID), "EMAIL_ADDR": f"{login_id}-changed@example.com"},
    )

    assert patch_resp.status_code == 200
    body = patch_resp.json()
    assert body["ROLE_ID"] == str(viewer_role.ROLE_ID)
    assert body["EMAIL_ADDR"] == f"{login_id}-changed@example.com"
    assert body["USER_LGID"] == login_id  # 로그인 ID는 수정 대상에서 제외


def test_patch_user_not_found_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.patch(
        f"/api/v1/users/{uuid.uuid4()}", headers=headers, json={"EMAIL_ADDR": "nobody@example.com"}
    )

    assert resp.status_code == 404


def test_patch_user_duplicate_email_returns_409(client, admin_token, admin_role):
    headers = {"Authorization": f"Bearer {admin_token}"}
    login_id_a = f"pytest_{uuid.uuid4().hex[:8]}"
    login_id_b = f"pytest_{uuid.uuid4().hex[:8]}"
    client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "USER_LGID": login_id_a,
            "EMAIL_ADDR": f"{login_id_a}@example.com",
            "password": "Str0ng!Pass",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )
    create_b = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "USER_LGID": login_id_b,
            "EMAIL_ADDR": f"{login_id_b}@example.com",
            "password": "Str0ng!Pass",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )

    patch_resp = client.patch(
        f"/api/v1/users/{create_b.json()['USER_ID']}",
        headers=headers,
        json={"EMAIL_ADDR": f"{login_id_a}@example.com"},
    )

    assert patch_resp.status_code == 409


def test_viewer_cannot_patch_user(client, viewer_token, admin_token, admin_role):
    """설계서(SCR-015) 접근 권한이 "A(Admin 전용)"이므로 VIEWER는 수정도 403이어야 한다."""
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    login_id = f"pytest_{uuid.uuid4().hex[:8]}"
    create_resp = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "USER_LGID": login_id,
            "EMAIL_ADDR": f"{login_id}@example.com",
            "password": "Str0ng!Pass",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )
    user_id = create_resp.json()["USER_ID"]

    viewer_headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.patch(
        f"/api/v1/users/{user_id}", headers=viewer_headers, json={"EMAIL_ADDR": "viewer-try@example.com"}
    )

    assert resp.status_code == 403


def test_delete_user_deactivates_and_rejects_second_call(client, admin_token, admin_role):
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
    user_id = create_resp.json()["USER_ID"]

    first = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert first.status_code == 200
    assert first.json()["USE_YN"] is False

    second = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert second.status_code == 409


def test_delete_user_not_found_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.delete(f"/api/v1/users/{uuid.uuid4()}", headers=headers)

    assert resp.status_code == 404


def test_viewer_cannot_delete_user(client, viewer_token, admin_token, admin_role):
    """설계서(SCR-015) 접근 권한이 "A(Admin 전용)"이므로 VIEWER는 비활성화도 403이어야 한다."""
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    login_id = f"pytest_{uuid.uuid4().hex[:8]}"
    create_resp = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "USER_LGID": login_id,
            "EMAIL_ADDR": f"{login_id}@example.com",
            "password": "Str0ng!Pass",
            "ROLE_ID": str(admin_role.ROLE_ID),
        },
    )
    user_id = create_resp.json()["USER_ID"]

    viewer_headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.delete(f"/api/v1/users/{user_id}", headers=viewer_headers)

    assert resp.status_code == 403


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
