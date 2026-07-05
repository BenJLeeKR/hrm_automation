import uuid

from sqlalchemy import select

from app.core.security import hash_password
from app.models.hr_empl_mst import HrEmplMst
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst


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


def _create_empl_linked_user(db_session, *, empl_role: SysRoleMst, dept, jikgup) -> SysUserMst:
    """`EMPL_ID`가 연결된 계정 — 사원 등록 시 자동 생성되는 계정을 흉내낸다(§8 큐 1-2)."""
    empl_no = f"PYTESTHRM{uuid.uuid4().hex[:6]}"
    employee = HrEmplMst(
        EMPL_NO=empl_no,
        EMPL_NM="HR_MGR권한테스트",
        EMAIL_ADDR=f"{empl_no}@example.com",
        DEPT_ID=dept.DEPT_ID,
        JIKGUP_ID=jikgup.JIKGUP_ID,
        EMPL_STAT_CD="ACTIVE",
    )
    db_session.add(employee)
    db_session.flush()

    user = SysUserMst(
        EMPL_ID=employee.EMPL_ID,
        USER_LGID=employee.EMAIL_ADDR,
        EMAIL_ADDR=employee.EMAIL_ADDR,
        ENCR_PWD=hash_password("Str0ng!Pass"),
        ROLE_ID=empl_role.ROLE_ID,
    )
    db_session.add(user)
    db_session.flush()
    return user


def test_hr_mgr_can_change_role_of_linked_account(client, db_session, hr_mgr_token, employee_role, dept, jikgup):
    """`HR_MGR`은 `EMPL_ID` 연결 계정의 업무 역할(PM/TEAM_LEAD/EXEC/EMPLOYEE/VIEWER)을
    변경할 수 있어야 한다 (설계서 §5.5 "직원 역할 배정", §8 큐 1-4)."""
    user = _create_empl_linked_user(db_session, empl_role=employee_role, dept=dept, jikgup=jikgup)
    pm_role = db_session.scalar(select(SysRoleMst).where(SysRoleMst.ROLE_CD == "PM"))

    headers = {"Authorization": f"Bearer {hr_mgr_token}"}
    resp = client.patch(f"/api/v1/users/{user.USER_ID}", headers=headers, json={"ROLE_ID": str(pm_role.ROLE_ID)})

    assert resp.status_code == 200
    assert resp.json()["ROLE_ID"] == str(pm_role.ROLE_ID)


def test_hr_mgr_cannot_promote_to_admin(client, db_session, hr_mgr_token, admin_role, employee_role, dept, jikgup):
    """`HR_MGR`은 `ADMIN` 역할로 승격시킬 수 없어야 한다."""
    user = _create_empl_linked_user(db_session, empl_role=employee_role, dept=dept, jikgup=jikgup)

    headers = {"Authorization": f"Bearer {hr_mgr_token}"}
    resp = client.patch(f"/api/v1/users/{user.USER_ID}", headers=headers, json={"ROLE_ID": str(admin_role.ROLE_ID)})

    assert resp.status_code == 403


def test_hr_mgr_cannot_modify_account_without_empl_id(client, admin_token, hr_mgr_token, admin_role):
    """`HR_MGR`은 사원과 연동되지 않은(`EMPL_ID` 없는) 시스템/외부 협력사 계정을 수정할
    수 없어야 한다."""
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

    hr_mgr_headers = {"Authorization": f"Bearer {hr_mgr_token}"}
    resp = client.patch(f"/api/v1/users/{user_id}", headers=hr_mgr_headers, json={"ROLE_ID": str(admin_role.ROLE_ID)})

    assert resp.status_code == 403


def test_hr_mgr_cannot_change_email_of_linked_account(client, db_session, hr_mgr_token, employee_role, dept, jikgup):
    """`HR_MGR`은 `EMPL_ID` 연결 계정이라도 업무 역할(`ROLE_ID`) 외 다른 필드는 수정할 수
    없어야 한다."""
    user = _create_empl_linked_user(db_session, empl_role=employee_role, dept=dept, jikgup=jikgup)

    headers = {"Authorization": f"Bearer {hr_mgr_token}"}
    resp = client.patch(f"/api/v1/users/{user.USER_ID}", headers=headers, json={"EMAIL_ADDR": "changed@example.com"})

    assert resp.status_code == 403
