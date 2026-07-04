import uuid


def test_create_patch_skill(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    skill_nm = f"PYTEST-SKILL-{uuid.uuid4().hex[:6]}"

    create_resp = client.post(
        "/api/v1/skills", headers=headers, json={"SKILL_NM": skill_nm, "SKILL_GRP_CD": "LANGUAGE"}
    )
    assert create_resp.status_code == 201
    skill_id = create_resp.json()["SKILL_ID"]
    assert create_resp.json()["USE_YN"] is True

    patch_resp = client.patch(f"/api/v1/skills/{skill_id}", headers=headers, json={"USE_YN": False})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["USE_YN"] is False


def test_duplicate_skill_grp_and_name_returns_409(client, admin_token):
    """HR_SKILL_MST(SKILL_GRP_CD, SKILL_NM) 복합 유니크 제약 회귀 테스트 —
    로드맵 §9 리스크 "SKILL_NM에 유니크 제약 없음" 해소 확인용."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"SKILL_NM": f"PYTEST-SKILL-{uuid.uuid4().hex[:6]}", "SKILL_GRP_CD": "LANGUAGE"}

    first = client.post("/api/v1/skills", headers=headers, json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/skills", headers=headers, json=payload)
    assert second.status_code == 409


def test_same_name_different_group_is_allowed(client, admin_token):
    """(SKILL_GRP_CD, SKILL_NM) 복합 유니크이므로 그룹이 다르면 동일 이름도 허용되어야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    name = f"PYTEST-SKILL-{uuid.uuid4().hex[:6]}"

    first = client.post("/api/v1/skills", headers=headers, json={"SKILL_NM": name, "SKILL_GRP_CD": "LANGUAGE"})
    second = client.post("/api/v1/skills", headers=headers, json={"SKILL_NM": name, "SKILL_GRP_CD": "BACKEND"})

    assert first.status_code == 201
    assert second.status_code == 201


def test_viewer_cannot_view_skills(client, viewer_token):
    """설계서(SCR-005) 화면 접근 권한이 "A H"이며 VIEWER는 제외되어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/skills", headers=headers)

    assert resp.status_code == 403
