import uuid


def test_create_list_patch_retire_employee(client, admin_token, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_no = f"PYTEST{uuid.uuid4().hex[:6]}"

    create_resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "테스트사원",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert create_resp.status_code == 201
    empl_id = create_resp.json()["EMPL_ID"]

    list_resp = client.get("/api/v1/employees", headers=headers, params={"dept_id": str(dept.DEPT_ID)})
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] == 1

    patch_resp = client.patch(f"/api/v1/employees/{empl_id}", headers=headers, json={"EMPL_NM": "수정된이름"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["EMPL_NM"] == "수정된이름"

    retire_resp = client.delete(f"/api/v1/employees/{empl_id}", headers=headers)
    assert retire_resp.status_code == 200
    assert retire_resp.json()["EMPL_STAT_CD"] == "RETIRED"

    retire_again_resp = client.delete(f"/api/v1/employees/{empl_id}", headers=headers)
    assert retire_again_resp.status_code == 409


def test_duplicate_empl_no_returns_409(client, admin_token, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_no = f"PYTEST{uuid.uuid4().hex[:6]}"
    payload = {
        "EMPL_NO": empl_no,
        "EMPL_NM": "중복사원",
        "EMAIL_ADDR": f"{empl_no}@example.com",
        "DEPT_ID": str(dept.DEPT_ID),
        "JIKGUP_ID": str(jikgup.JIKGUP_ID),
    }

    first = client.post("/api/v1/employees", headers=headers, json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/employees", headers=headers, json=payload)
    assert second.status_code == 409


def test_patch_nonexistent_employee_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.patch(f"/api/v1/employees/{uuid.uuid4()}", headers=headers, json={"EMPL_NM": "없음"})

    assert resp.status_code == 404


def test_viewer_cannot_create_employee(client, viewer_token, dept, jikgup):
    """VIEWER 역할은 PERM_JSON상 employees.create 권한이 없어 403이어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    empl_no = f"PYTEST{uuid.uuid4().hex[:6]}"

    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "권한테스트",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )

    assert resp.status_code == 403


def test_viewer_can_view_employees(client, viewer_token):
    """VIEWER 역할은 PERM_JSON상 employees.view 권한이 있어 조회는 가능해야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}

    resp = client.get("/api/v1/employees", headers=headers)

    assert resp.status_code == 200


def test_get_employee_detail(client, admin_token, dept, jikgup):
    """사원 상세 조회 (SCR-004) — 등록한 사원의 GET /employees/{empl_id} 응답 확인"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_no = f"PYTEST{uuid.uuid4().hex[:6]}"

    create_resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "상세조회테스트",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert create_resp.status_code == 201
    empl_id = create_resp.json()["EMPL_ID"]

    detail_resp = client.get(f"/api/v1/employees/{empl_id}", headers=headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["EMPL_NO"] == empl_no
    assert detail_resp.json()["EMPL_NM"] == "상세조회테스트"


def test_get_employee_detail_not_found_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get(f"/api/v1/employees/{uuid.uuid4()}", headers=headers)

    assert resp.status_code == 404


def test_viewer_can_view_employee_detail(client, viewer_token, admin_token, dept, jikgup):
    """VIEWER 역할도 employees.view 권한으로 사원 상세를 조회할 수 있어야 한다."""
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    empl_no = f"PYTEST{uuid.uuid4().hex[:6]}"
    create_resp = client.post(
        "/api/v1/employees",
        headers=admin_headers,
        json={
            "EMPL_NO": empl_no,
            "EMPL_NM": "뷰어조회테스트",
            "EMAIL_ADDR": f"{empl_no}@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    empl_id = create_resp.json()["EMPL_ID"]

    viewer_headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get(f"/api/v1/employees/{empl_id}", headers=viewer_headers)

    assert resp.status_code == 200
