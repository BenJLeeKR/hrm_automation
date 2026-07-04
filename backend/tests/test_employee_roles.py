import uuid

from sqlalchemy import select

from app.models.hr_empl_role_rel import HrEmplRoleRel
from app.models.hr_jikmu_mst import HrJikmuMst


def _create_employee(client, headers, dept, jikgup) -> str:
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": f"PYTESTROLE{uuid.uuid4().hex[:6]}",
            "EMPL_NM": "역할테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def test_list_employee_roles_filters_by_empl_id(client, admin_token, db_session, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)
    other_empl_id = _create_employee(client, headers, dept, jikgup)
    jikmu = db_session.scalars(select(HrJikmuMst).limit(1)).first()

    db_session.add(HrEmplRoleRel(EMPL_ID=uuid.UUID(empl_id), JIKMU_ID=jikmu.JIKMU_ID, IS_PRIMARY=True))
    db_session.add(HrEmplRoleRel(EMPL_ID=uuid.UUID(other_empl_id), JIKMU_ID=jikmu.JIKMU_ID, IS_PRIMARY=True))
    db_session.flush()

    resp = client.get("/api/v1/employee-roles", headers=headers, params={"empl_id": empl_id})

    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["EMPL_ID"] == empl_id
    assert body[0]["JIKMU_ID"] == str(jikmu.JIKMU_ID)


def test_viewer_can_list_employee_roles(client, viewer_token):
    headers = {"Authorization": f"Bearer {viewer_token}"}
    resp = client.get("/api/v1/employee-roles", headers=headers)

    assert resp.status_code == 200


def test_patch_jikmu_id_syncs_primary_role_rel(client, admin_token, db_session, dept, jikgup):
    """사원 목록 "보유 역할" 배지는 `HR_EMPL_ROLE_REL`을 조회하므로, `PATCH .../employees`로
    `JIKMU_ID`(주 직무)만 바꿔도 기존 IS_PRIMARY 행이 새 직무 유형으로 함께 갱신되어야
    한다 — 그렇지 않으면 목록에 옛 직무 유형이 계속 표시된다(사용자 리포트로 발견한 버그)."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    jikmu_a, jikmu_b = db_session.scalars(select(HrJikmuMst).limit(2)).all()
    empl_id = _create_employee(client, headers, dept, jikgup)

    db_session.add(HrEmplRoleRel(EMPL_ID=uuid.UUID(empl_id), JIKMU_ID=jikmu_a.JIKMU_ID, IS_PRIMARY=True))
    db_session.commit()

    resp = client.patch(
        f"/api/v1/employees/{empl_id}",
        headers=headers,
        json={"JIKMU_ID": str(jikmu_b.JIKMU_ID)},
    )
    assert resp.status_code == 200

    roles = db_session.scalars(
        select(HrEmplRoleRel).where(HrEmplRoleRel.EMPL_ID == uuid.UUID(empl_id))
    ).all()
    assert len(roles) == 1
    assert roles[0].JIKMU_ID == jikmu_b.JIKMU_ID
    assert roles[0].IS_PRIMARY is True
