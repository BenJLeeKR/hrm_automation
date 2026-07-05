"""`HR_DATA_QUALITY_CHK` 배치(로드맵 §8, `app/services/data_quality_chk.py`) 검증.

`PJT_ASGN_END_ALERT` 테스트(`test_asgn_end_alert.py`)와 동일한 이유로 실 서버 DB에는
이미 목데이터가 있어 절대값 비교 대신 실행 전/후 비교로 검증한다. Teams 알림은
`TEAMS_WEBHOOK_URL`이 비어 있어 실제 전송을 시도하지 않는다.
"""

import uuid
from datetime import date

from sqlalchemy import select

from app.core.config import settings
from app.models.pjt_mst import PjtMst
from app.models.sys_batch_his import SysBatchHis
from app.services.data_quality_chk import run_data_quality_chk


def _create_employee(client, headers, dept, jikgup) -> str:
    """기술·직무 유형을 등록하지 않은 사원 — 품질 점검의 "기술/직무 미등록" 카운트에
    잡혀야 한다."""
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": f"PYTESTDQ{uuid.uuid4().hex[:6]}",
            "EMPL_NM": "품질점검테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def _create_project(db_session) -> PjtMst:
    project = PjtMst(
        PJT_ID=uuid.uuid4(),
        PJT_CD=f"PYTESTDQ-{uuid.uuid4().hex[:8]}",
        PJT_NM="품질점검테스트프로젝트",
        PJT_STAT_CD="RUNNING",
        STRT_DT=date(2026, 1, 1),
    )
    db_session.add(project)
    db_session.flush()
    return project


def test_run_data_quality_chk_counts_skill_and_job_missing(client, admin_token, db_session, dept, jikgup, monkeypatch):
    monkeypatch.setattr(settings, "TEAMS_WEBHOOK_URL", "")
    headers = {"Authorization": f"Bearer {admin_token}"}
    before = run_data_quality_chk(db_session)

    _create_employee(client, headers, dept, jikgup)

    after = run_data_quality_chk(db_session)

    assert after.EXEC_STAT_CD == "SUCCESS"
    assert after.BATCH_NM == "HR_DATA_QUALITY_CHK"
    assert after.CRT_CNT == before.CRT_CNT + 2  # 기술 미등록 +1, 직무 미등록 +1
    assert "TEAMS_WEBHOOK_URL 미설정" in after.RSLT_SUMR

    saved_history = db_session.scalar(select(SysBatchHis).where(SysBatchHis.BATCH_ID == after.BATCH_ID))
    assert saved_history is not None


def test_run_data_quality_chk_counts_missing_end_date(client, admin_token, db_session, dept, jikgup, monkeypatch):
    monkeypatch.setattr(settings, "TEAMS_WEBHOOK_URL", "")
    headers = {"Authorization": f"Bearer {admin_token}"}
    before = run_data_quality_chk(db_session)

    empl_id = _create_employee(client, headers, dept, jikgup)
    project = _create_project(db_session)
    resp = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "EMPL_ID": empl_id,
            "PJT_ID": str(project.PJT_ID),
            "PRJT_ROLE_NM": "Backend",
            "ALLOC_RT": 50,
            "ASGN_STRT_DT": "2026-06-01",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert resp.status_code == 201

    after = run_data_quality_chk(db_session)

    # 기술 미등록 +1, 직무 미등록 +1, 종료일 누락 +1
    assert after.CRT_CNT == before.CRT_CNT + 3
