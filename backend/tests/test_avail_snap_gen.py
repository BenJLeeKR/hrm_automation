"""`HR_AVAIL_SNAP_GEN` 배치(로드맵 §8, `app/services/avail_snap_gen.py`) 검증."""

import uuid
from datetime import date

from sqlalchemy import select

from app.models.hr_avail_snap import HrAvailSnap
from app.models.sys_batch_his import SysBatchHis
from app.services.avail_snap_gen import run_avail_snap_gen


def _create_employee(client, headers, dept, jikgup) -> str:
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": f"PYTESTSNAP{uuid.uuid4().hex[:6]}",
            "EMPL_NM": "스냅샷테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def test_run_avail_snap_gen_creates_snapshot_and_batch_history(client, admin_token, db_session, dept, jikgup):
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)
    snap_dt = date(2026, 7, 4)

    history = run_avail_snap_gen(db_session, snap_dt=snap_dt)

    assert history.EXEC_STAT_CD == "SUCCESS"
    assert history.BATCH_NM == "HR_AVAIL_SNAP_GEN"
    assert history.CRT_CNT is not None and history.CRT_CNT >= 1

    snap = db_session.scalar(
        select(HrAvailSnap).where(HrAvailSnap.EMPL_ID == uuid.UUID(empl_id), HrAvailSnap.SNAP_DT == snap_dt)
    )
    assert snap is not None
    assert snap.AVAIL_STAT_CD == "AVAILABLE"
    assert snap.TOT_ALLOC_RT == 0

    saved_history = db_session.scalar(select(SysBatchHis).where(SysBatchHis.BATCH_ID == history.BATCH_ID))
    assert saved_history is not None


def test_run_avail_snap_gen_is_idempotent_for_same_date(client, admin_token, db_session, dept, jikgup):
    """같은 날짜로 재실행해도(배치 수동 재실행 대비) 스냅샷이 중복 생성되지 않아야 한다."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    empl_id = _create_employee(client, headers, dept, jikgup)
    snap_dt = date(2026, 7, 4)

    run_avail_snap_gen(db_session, snap_dt=snap_dt)
    run_avail_snap_gen(db_session, snap_dt=snap_dt)

    snaps = list(
        db_session.scalars(
            select(HrAvailSnap).where(HrAvailSnap.EMPL_ID == uuid.UUID(empl_id), HrAvailSnap.SNAP_DT == snap_dt)
        )
    )
    assert len(snaps) == 1
