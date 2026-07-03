import uuid


def test_create_list_patch_project(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    pjt_cd = f"PYTEST{uuid.uuid4().hex[:6]}".upper()

    create_resp = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"PJT_CD": pjt_cd, "PJT_NM": "테스트프로젝트", "STRT_DT": "2026-01-01"},
    )
    assert create_resp.status_code == 201
    pjt_id = create_resp.json()["PJT_ID"]

    list_resp = client.get("/api/v1/projects", headers=headers)
    assert list_resp.status_code == 200

    patch_resp = client.patch(
        f"/api/v1/projects/{pjt_id}", headers=headers, json={"PJT_NM": "수정된프로젝트"}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["PJT_NM"] == "수정된프로젝트"


def test_get_project_detail(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    pjt_cd = f"PYTEST{uuid.uuid4().hex[:6]}".upper()

    create_resp = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"PJT_CD": pjt_cd, "PJT_NM": "상세조회테스트", "STRT_DT": "2026-01-01"},
    )
    pjt_id = create_resp.json()["PJT_ID"]

    detail_resp = client.get(f"/api/v1/projects/{pjt_id}", headers=headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["PJT_CD"] == pjt_cd


def test_get_project_detail_not_found_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get(f"/api/v1/projects/{uuid.uuid4()}", headers=headers)

    assert resp.status_code == 404


def test_duplicate_pjt_cd_returns_409(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"PJT_CD": f"PYTEST{uuid.uuid4().hex[:6]}".upper(), "PJT_NM": "중복프로젝트", "STRT_DT": "2026-01-01"}

    first = client.post("/api/v1/projects", headers=headers, json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/projects", headers=headers, json=payload)
    assert second.status_code == 409


def test_viewer_can_view_project_detail(client, viewer_token, admin_token):
    """VIEWER 역할도 projects.view 권한으로 프로젝트 상세를 조회할 수 있어야 한다."""
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    create_resp = client.post(
        "/api/v1/projects",
        headers=admin_headers,
        json={"PJT_CD": f"PYTEST{uuid.uuid4().hex[:6]}".upper(), "PJT_NM": "뷰어조회테스트", "STRT_DT": "2026-01-01"},
    )
    pjt_id = create_resp.json()["PJT_ID"]

    viewer_headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get(f"/api/v1/projects/{pjt_id}", headers=viewer_headers)

    assert resp.status_code == 200
