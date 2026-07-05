"""계정 없는 기존 사원 백필 스크립트(`app/db/backfill_employee_accounts.py`) 검증 —
사원-계정 연동 설계 반영(§8 큐 1번) 후속 데이터 마이그레이션 작업(운영팀 요청, 2026-07-06).
"""

import uuid

from sqlalchemy import select

from app.core.config import settings
from app.core.security import verify_password
from app.db.backfill_employee_accounts import backfill_missing_accounts
from app.models.hr_empl_mst import HrEmplMst
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst


def _create_unlinked_employee(db_session, dept, jikgup, *, empl_stat_cd: str = "ACTIVE") -> HrEmplMst:
    empl_no = f"PYTESTBACKFILL{uuid.uuid4().hex[:6]}"
    employee = HrEmplMst(
        EMPL_NO=empl_no,
        EMPL_NM="백필테스트",
        EMAIL_ADDR=f"{empl_no}@example.com",
        DEPT_ID=dept.DEPT_ID,
        JIKGUP_ID=jikgup.JIKGUP_ID,
        EMPL_STAT_CD=empl_stat_cd,
    )
    db_session.add(employee)
    db_session.flush()
    return employee


def test_backfill_creates_account_for_unlinked_employee(db_session, dept, jikgup):
    employee = _create_unlinked_employee(db_session, dept, jikgup)

    result = backfill_missing_accounts(db_session)

    assert result["failed_count"] == 0
    created_empl_nos = {item["EMPL_NO"] for item in result["created"]}
    assert employee.EMPL_NO in created_empl_nos

    user = db_session.scalar(select(SysUserMst).where(SysUserMst.EMPL_ID == employee.EMPL_ID))
    assert user is not None
    assert user.USER_LGID == employee.EMAIL_ADDR
    assert user.PWD_CHG_YN is True
    role = db_session.get(SysRoleMst, user.ROLE_ID)
    assert role.ROLE_CD == "EMPLOYEE"

    created_item = next(item for item in result["created"] if item["EMPL_NO"] == employee.EMPL_NO)
    assert verify_password(created_item["temp_password"], user.ENCR_PWD)


def test_backfill_skips_already_linked_employee(db_session, dept, jikgup):
    employee = _create_unlinked_employee(db_session, dept, jikgup)
    first_run = backfill_missing_accounts(db_session)
    assert employee.EMPL_NO in {item["EMPL_NO"] for item in first_run["created"]}

    second_run = backfill_missing_accounts(db_session)

    assert employee.EMPL_NO not in {item["EMPL_NO"] for item in second_run["created"]}


def test_backfill_excludes_retired_employee(db_session, dept, jikgup):
    employee = _create_unlinked_employee(db_session, dept, jikgup, empl_stat_cd="RETIRED")

    result = backfill_missing_accounts(db_session)

    assert employee.EMPL_NO not in {item["EMPL_NO"] for item in result["created"]}
    user = db_session.scalar(select(SysUserMst).where(SysUserMst.EMPL_ID == employee.EMPL_ID))
    assert user is None


def test_backfill_uses_env_initial_password_when_set(db_session, dept, jikgup, monkeypatch):
    monkeypatch.setattr(settings, "EMPLOYEE_INITIAL_PASSWORD", "Fixed!Init123")
    employee = _create_unlinked_employee(db_session, dept, jikgup)

    result = backfill_missing_accounts(db_session)

    created_item = next(item for item in result["created"] if item["EMPL_NO"] == employee.EMPL_NO)
    assert created_item["temp_password"] == "Fixed!Init123"
