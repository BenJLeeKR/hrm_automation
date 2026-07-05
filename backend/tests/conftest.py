"""Pytest 공통 픽스처 (로드맵 §8 "Pytest 단위 테스트 스위트 구축", Phase 3 완료 기준).

테스트는 별도 테스트 DB를 두지 않고, `.env`에 설정된 실제 개발 DB에 연결하되
"연결(connection) 하나 + 외부 트랜잭션 + 세션은 SAVEPOINT로 커밋"하는 표준 패턴을
사용한다. 애플리케이션 코드가 각 API 호출 안에서 `db.commit()`을 호출해도 이는
SAVEPOINT만 커밋할 뿐이며, 테스트가 끝나면 외부 트랜잭션을 롤백해 DB에는 어떤
흔적도 남기지 않는다 — 이 프로젝트 전반에서 실 서버 검증 후 항상 임시 데이터를
수동으로 삭제해온 것과 같은 목적을, 테스트에서는 트랜잭션 롤백으로 자동화한 것이다.
"""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import create_access_token, hash_password
from app.db.session import get_db
from app.main import app
from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_jikgup_mst import HrJikgupMst
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst

_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

TEST_PASSWORD = "Test1234!"


@pytest.fixture()
def db_session():
    connection = _engine.connect()
    outer_trans = connection.begin()
    session = sessionmaker(bind=connection, join_transaction_mode="create_savepoint")()
    try:
        yield session
    finally:
        session.close()
        outer_trans.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _get_role(db_session, role_cd: str) -> SysRoleMst:
    role = db_session.scalar(select(SysRoleMst).where(SysRoleMst.ROLE_CD == role_cd))
    if role is None:
        pytest.skip(f"SYS_ROLE_MST에 {role_cd} Seed가 없습니다 — Alembic Seed 마이그레이션 적용 후 실행하세요.")
    return role


@pytest.fixture()
def admin_role(db_session) -> SysRoleMst:
    return _get_role(db_session, "ADMIN")


@pytest.fixture()
def viewer_role(db_session) -> SysRoleMst:
    return _get_role(db_session, "VIEWER")


@pytest.fixture()
def hr_mgr_role(db_session) -> SysRoleMst:
    return _get_role(db_session, "HR_MGR")


@pytest.fixture()
def employee_role(db_session) -> SysRoleMst:
    return _get_role(db_session, "EMPLOYEE")


@pytest.fixture()
def dept(db_session) -> HrDeptMst:
    dept = HrDeptMst(DEPT_ID=uuid.uuid4(), DEPT_CD=f"PYTEST-{uuid.uuid4().hex[:8]}", DEPT_NM="테스트부서")
    db_session.add(dept)
    db_session.flush()
    return dept


@pytest.fixture()
def jikgup(db_session) -> HrJikgupMst:
    jikgup = db_session.scalar(select(HrJikgupMst))
    if jikgup is None:
        pytest.skip("HR_JIKGUP_MST Seed가 없습니다 — Alembic Seed 마이그레이션 적용 후 실행하세요.")
    return jikgup


def create_user_with_password(db_session, role: SysRoleMst, *, password: str = TEST_PASSWORD) -> tuple[str, str]:
    """로그인 API 테스트용 — 로그인 ID/비밀번호 평문 쌍을 반환한다."""
    login_id = f"pytest_{uuid.uuid4().hex[:10]}"
    user = SysUserMst(
        USER_ID=uuid.uuid4(),
        USER_LGID=login_id,
        EMAIL_ADDR=f"{login_id}@example.com",
        ENCR_PWD=hash_password(password),
        ROLE_ID=role.ROLE_ID,
    )
    db_session.add(user)
    db_session.flush()
    return login_id, password


def _make_token_user(db_session, role: SysRoleMst) -> SysUserMst:
    login_id, _ = create_user_with_password(db_session, role)
    return db_session.scalar(select(SysUserMst).where(SysUserMst.USER_LGID == login_id))


@pytest.fixture()
def admin_token(db_session, admin_role) -> str:
    user = _make_token_user(db_session, admin_role)
    return create_access_token(user_id=str(user.USER_ID), role_id=str(user.ROLE_ID))


@pytest.fixture()
def viewer_token(db_session, viewer_role) -> str:
    user = _make_token_user(db_session, viewer_role)
    return create_access_token(user_id=str(user.USER_ID), role_id=str(user.ROLE_ID))


@pytest.fixture()
def hr_mgr_token(db_session, hr_mgr_role) -> str:
    user = _make_token_user(db_session, hr_mgr_role)
    return create_access_token(user_id=str(user.USER_ID), role_id=str(user.ROLE_ID))
