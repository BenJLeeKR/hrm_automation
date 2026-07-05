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


def test_list_audit_logs_filters_by_tgt_id(client, admin_token, dept, jikgup):
    """사원 상세 화면(SCR-004) "변경 이력" 탭이 특정 사원 1명의 이력만 조회할 수 있어야
    한다(§9-1) — 사원 등록(CREATE) 자체가 감사 로그를 남기므로 그 사원의 TGT_ID로
    필터링하면 다른 사원의 로그와 섞이지 않고 해당 건만 반환되는지 확인한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    create_resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": "PYTESTAUDIT01",
            "EMPL_NM": "감사로그테스트",
            "EMAIL_ADDR": "pytestaudit01@example.com",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert create_resp.status_code == 201
    empl_id = create_resp.json()["EMPL_ID"]

    resp = client.get(
        "/api/v1/audit-logs",
        headers=headers,
        params={"tgt_tbl_nm": "HR_EMPL_MST", "tgt_id": empl_id},
    )

    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) >= 1
    assert all(item["TGT_ID"] == empl_id for item in items)


def test_export_audit_logs_returns_xlsx(client, admin_token):
    """§9-1 "감사 로그 Excel 내보내기" — 화면 조회 API와 동일한 필터로 전체 행을 xlsx로 내려준다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/audit-logs/export", headers=headers, params={"act_cd": "LOGIN"})

    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert "audit_logs_" in resp.headers["content-disposition"]


def test_viewer_cannot_export_audit_logs(client, viewer_token):
    """설계서(SCR-016) 접근 권한이 "A(Admin 전용)"이므로 VIEWER는 내보내기도 403이어야 한다."""
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/audit-logs/export", headers=headers)

    assert resp.status_code == 403
