from tests.conftest import TEST_PASSWORD, create_user_with_password


def test_login_success(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)

    resp = client.post("/api/v1/auth/login", json={"USER_LGID": login_id, "password": password})

    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client, db_session, admin_role):
    login_id, _ = create_user_with_password(db_session, admin_role)

    resp = client.post("/api/v1/auth/login", json={"USER_LGID": login_id, "password": "wrong-password"})

    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    resp = client.post("/api/v1/auth/login", json={"USER_LGID": "no-such-user", "password": "whatever"})

    assert resp.status_code == 401


def test_refresh_token_issues_new_access_token(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)
    login_resp = client.post("/api/v1/auth/login", json={"USER_LGID": login_id, "password": password})
    refresh_token = login_resp.json()["refresh_token"]

    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})

    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_refresh_rejects_access_token(client, db_session, admin_role):
    """액세스 토큰을 리프레시 토큰으로 오용하면 토큰 타입 검증에서 거부되어야 한다."""
    login_id, password = create_user_with_password(db_session, admin_role)
    login_resp = client.post("/api/v1/auth/login", json={"USER_LGID": login_id, "password": password})
    access_token = login_resp.json()["access_token"]

    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": access_token})

    assert resp.status_code == 401


def test_protected_endpoint_requires_auth(client):
    resp = client.get("/api/v1/employees")

    assert resp.status_code == 401


def test_protected_endpoint_rejects_garbage_token(client):
    resp = client.get("/api/v1/employees", headers={"Authorization": "Bearer garbage"})

    assert resp.status_code == 401


def test_me_returns_current_user_and_perm_json(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)
    access_token = client.post(
        "/api/v1/auth/login", json={"USER_LGID": login_id, "password": password}
    ).json()["access_token"]

    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["USER_LGID"] == login_id
    assert body["ROLE_CD"] == "ADMIN"
    assert body["PERM_JSON"]["screens"]["employees"]["view"] is True


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/me")

    assert resp.status_code == 401


def test_update_me_changes_own_email(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)
    access_token = client.post(
        "/api/v1/auth/login", json={"USER_LGID": login_id, "password": password}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    resp = client.patch("/api/v1/auth/me", headers=headers, json={"EMAIL_ADDR": f"{login_id}-new@example.com"})

    assert resp.status_code == 200
    assert resp.json()["EMAIL_ADDR"] == f"{login_id}-new@example.com"

    get_resp = client.get("/api/v1/auth/me", headers=headers)
    assert get_resp.json()["EMAIL_ADDR"] == f"{login_id}-new@example.com"


def test_update_me_duplicate_email_conflict(client, db_session, admin_role):
    other_login_id, _ = create_user_with_password(db_session, admin_role)
    login_id, password = create_user_with_password(db_session, admin_role)
    access_token = client.post(
        "/api/v1/auth/login", json={"USER_LGID": login_id, "password": password}
    ).json()["access_token"]

    resp = client.patch(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"EMAIL_ADDR": f"{other_login_id}@example.com"},
    )

    assert resp.status_code == 409


def test_update_me_requires_auth(client):
    resp = client.patch("/api/v1/auth/me", json={"EMAIL_ADDR": "no-auth@example.com"})

    assert resp.status_code == 401


def test_change_password_success_and_relogin(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)
    access_token = client.post(
        "/api/v1/auth/login", json={"USER_LGID": login_id, "password": password}
    ).json()["access_token"]

    resp = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"current_password": password, "new_password": "NewStr0ng!Pass"},
    )
    assert resp.status_code == 204

    old_login = client.post("/api/v1/auth/login", json={"USER_LGID": login_id, "password": password})
    assert old_login.status_code == 401

    new_login = client.post("/api/v1/auth/login", json={"USER_LGID": login_id, "password": "NewStr0ng!Pass"})
    assert new_login.status_code == 200


def test_change_password_wrong_current_password(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)
    access_token = client.post(
        "/api/v1/auth/login", json={"USER_LGID": login_id, "password": password}
    ).json()["access_token"]

    resp = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"current_password": "wrong-password", "new_password": "NewStr0ng!Pass"},
    )
    assert resp.status_code == 401


def test_change_password_weak_new_password_rejected(client, db_session, admin_role):
    login_id, password = create_user_with_password(db_session, admin_role)
    access_token = client.post(
        "/api/v1/auth/login", json={"USER_LGID": login_id, "password": password}
    ).json()["access_token"]

    resp = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"current_password": password, "new_password": "weak"},
    )
    assert resp.status_code == 422


def test_change_password_requires_auth(client):
    resp = client.post(
        "/api/v1/auth/change-password",
        json={"current_password": TEST_PASSWORD, "new_password": "NewStr0ng!Pass"},
    )
    assert resp.status_code == 401
