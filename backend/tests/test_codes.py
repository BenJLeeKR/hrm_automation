import uuid


def test_create_patch_job_type(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    jikmu_cd = f"PYTEST{uuid.uuid4().hex[:6]}".upper()

    create_resp = client.post(
        "/api/v1/job-types",
        headers=headers,
        json={"JIKMU_CD": jikmu_cd, "JIKMU_NM": "테스트직무", "JIKMU_GRP_CD": "TECHNICAL"},
    )
    assert create_resp.status_code == 201
    jikmu_id = create_resp.json()["JIKMU_ID"]
    assert create_resp.json()["USE_YN"] is True

    list_resp = client.get("/api/v1/job-types", headers=headers, params={"use_yn": "true"})
    assert list_resp.status_code == 200
    assert any(j["JIKMU_ID"] == jikmu_id for j in list_resp.json())

    patch_resp = client.patch(
        f"/api/v1/job-types/{jikmu_id}", headers=headers, json={"JIKMU_NM": "수정된직무", "USE_YN": False}
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["JIKMU_NM"] == "수정된직무"
    assert patch_resp.json()["USE_YN"] is False


def test_duplicate_jikmu_cd_returns_409(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"JIKMU_CD": f"PYTEST{uuid.uuid4().hex[:6]}".upper(), "JIKMU_NM": "중복직무"}

    first = client.post("/api/v1/job-types", headers=headers, json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/job-types", headers=headers, json=payload)
    assert second.status_code == 409


def test_patch_nonexistent_job_type_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.patch(f"/api/v1/job-types/{uuid.uuid4()}", headers=headers, json={"JIKMU_NM": "없음"})

    assert resp.status_code == 404


def test_viewer_cannot_create_job_type(client, viewer_token):
    """VIEWER 역할은 PERM_JSON상 job_types.create 권한이 없어 403이어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}

    resp = client.post(
        "/api/v1/job-types",
        headers=headers,
        json={"JIKMU_CD": f"PYTEST{uuid.uuid4().hex[:6]}".upper(), "JIKMU_NM": "권한테스트"},
    )

    assert resp.status_code == 403


def test_viewer_can_view_job_types(client, viewer_token):
    """직무 유형 조회는 `codes.view` 정책으로 전 역할 허용되어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}

    resp = client.get("/api/v1/job-types", headers=headers)

    assert resp.status_code == 200
