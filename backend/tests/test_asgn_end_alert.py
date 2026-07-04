"""`PJT_ASGN_END_ALERT` 배치(로드맵 §8, `app/services/asgn_end_alert.py`) 검증.

Teams 알림은 로컬/테스트 환경에서 `TEAMS_WEBHOOK_URL`이 비어 있어(기본값) 실제 전송을
시도하지 않는다 — `send_teams_message`가 이 경우 조용히 `False`를 반환하는 동작 자체를
검증 대상으로 삼는다(실제 네트워크 호출은 하지 않음).
"""

import uuid
from datetime import date

from sqlalchemy import select

from app.core.config import settings
from app.models.pjt_mst import PjtMst
from app.models.sys_batch_his import SysBatchHis
from app.services.asgn_end_alert import run_asgn_end_alert


def _create_employee(client, headers, dept, jikgup) -> str:
    resp = client.post(
        "/api/v1/employees",
        headers=headers,
        json={
            "EMPL_NO": f"PYTESTALERT{uuid.uuid4().hex[:6]}",
            "EMPL_NM": "종료알림테스트",
            "DEPT_ID": str(dept.DEPT_ID),
            "JIKGUP_ID": str(jikgup.JIKGUP_ID),
        },
    )
    assert resp.status_code == 201
    return resp.json()["EMPL_ID"]


def _create_project(db_session) -> PjtMst:
    project = PjtMst(
        PJT_ID=uuid.uuid4(),
        PJT_CD=f"PYTESTALERT-{uuid.uuid4().hex[:8]}",
        PJT_NM="종료알림테스트프로젝트",
        PJT_STAT_CD="RUNNING",
        STRT_DT=date(2026, 1, 1),
    )
    db_session.add(project)
    db_session.flush()
    return project


def test_run_asgn_end_alert_counts_assignments_ending_within_30_days(
    client, admin_token, db_session, dept, jikgup, monkeypatch
):
    """이미 존재하는 목데이터 투입 이력과 섞여도(다른 화면 검증에서 이미 확인된 패턴과
    동일하게) 신규로 추가한 건만큼 카운트가 정확히 늘어나는지 전/후 비교로 검증한다 —
    실 서버 DB에는 이 배치가 스캔하는 `PJT_ASGN_HIS` 전체 테이블에 이미 목데이터가
    들어있어 절대값 비교는 신뢰할 수 없다."""
    monkeypatch.setattr(settings, "TEAMS_WEBHOOK_URL", "")
    headers = {"Authorization": f"Bearer {admin_token}"}
    as_of = date(2026, 7, 4)
    before = run_asgn_end_alert(db_session, as_of=as_of)

    empl_id = _create_employee(client, headers, dept, jikgup)
    project = _create_project(db_session)
    create_resp = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "EMPL_ID": empl_id,
            "PJT_ID": str(project.PJT_ID),
            "PRJT_ROLE_NM": "Backend",
            "ALLOC_RT": 100,
            "ASGN_STRT_DT": "2026-06-01",
            "ASGN_END_DT": "2026-07-20",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert create_resp.status_code == 201

    after = run_asgn_end_alert(db_session, as_of=as_of)

    assert after.EXEC_STAT_CD == "SUCCESS"
    assert after.BATCH_NM == "PJT_ASGN_END_ALERT"
    assert after.CRT_CNT == before.CRT_CNT + 1
    assert "TEAMS_WEBHOOK_URL 미설정" in after.RSLT_SUMR

    saved_history = db_session.scalar(select(SysBatchHis).where(SysBatchHis.BATCH_ID == after.BATCH_ID))
    assert saved_history is not None


def test_run_asgn_end_alert_excludes_assignment_beyond_30_days(
    client, admin_token, db_session, dept, jikgup, monkeypatch
):
    monkeypatch.setattr(settings, "TEAMS_WEBHOOK_URL", "")
    headers = {"Authorization": f"Bearer {admin_token}"}
    as_of = date(2026, 7, 4)
    before = run_asgn_end_alert(db_session, as_of=as_of)

    empl_id = _create_employee(client, headers, dept, jikgup)
    project = _create_project(db_session)
    resp = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "EMPL_ID": empl_id,
            "PJT_ID": str(project.PJT_ID),
            "PRJT_ROLE_NM": "Backend",
            "ALLOC_RT": 100,
            "ASGN_STRT_DT": "2026-06-01",
            "ASGN_END_DT": "2026-12-31",
            "ASGN_STAT_CD": "ACTIVE",
        },
    )
    assert resp.status_code == 201

    after = run_asgn_end_alert(db_session, as_of=as_of)

    assert after.CRT_CNT == before.CRT_CNT
