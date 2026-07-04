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
