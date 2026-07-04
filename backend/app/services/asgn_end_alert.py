from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.sys_batch_his import SysBatchHis
from app.repositories.pjt_asgn_his import list_ending_soon_assignments
from app.services.teams_notify import TeamsNotifyError, send_teams_message

BATCH_NAME = "PJT_ASGN_END_ALERT"
_ALERT_WINDOW_DAYS = 30


def _build_message(rows, *, as_of: date) -> str:
    if not rows:
        return f"[투입 종료 예정 알림] {as_of.isoformat()} 기준 {_ALERT_WINDOW_DAYS}일 이내 종료 예정 건이 없습니다."

    lines = [f"- {r.EMPL_NM}({r.EMPL_NO}) · {r.PJT_NM} · 종료 예정일 {r.ASGN_END_DT.isoformat()}" for r in rows]
    header = f"[투입 종료 예정 알림] {as_of.isoformat()} 기준 {_ALERT_WINDOW_DAYS}일 이내 종료 예정 {len(rows)}건"
    return "\n".join([header, *lines])


def run_asgn_end_alert(db: Session, *, as_of: date | None = None) -> SysBatchHis:
    """`PJT_ASGN_END_ALERT` 배치 실행기 (로드맵 §8, 설계서 §10 자동화 배치 — 매주 금요일
    17:00, 투입 종료 30일 이내 건 Teams 알림). 성공/실패 여부와 무관하게 `SYS_BATCH_HIS`에
    실행 이력을 남긴다 — `HR_AVAIL_SNAP_GEN`(`app/services/avail_snap_gen.py`)과 동일한
    실행/기록 패턴을 따른다.
    """
    target_dt = as_of or date.today()
    started_at = datetime.now(timezone.utc)

    rows = list_ending_soon_assignments(db, as_of=target_dt, within_days=_ALERT_WINDOW_DAYS)
    message = _build_message(rows, as_of=target_dt)

    try:
        sent = send_teams_message(message)
    except TeamsNotifyError as exc:
        db.rollback()
        history = SysBatchHis(
            BATCH_NM=BATCH_NAME,
            EXEC_STAT_CD="FAILED",
            EXEC_STRT_DTTM=started_at,
            EXEC_END_DTTM=datetime.now(timezone.utc),
            ERR_MSG=str(exc),
            CRT_CNT=0,
            FAIL_CNT=1,
        )
        db.add(history)
        db.commit()
        raise

    summary = f"{target_dt.isoformat()} 기준 종료 예정 {len(rows)}건 확인"
    if not sent:
        summary += " (TEAMS_WEBHOOK_URL 미설정 — 알림 전송 생략)"

    history = SysBatchHis(
        BATCH_NM=BATCH_NAME,
        EXEC_STAT_CD="SUCCESS",
        EXEC_STRT_DTTM=started_at,
        EXEC_END_DTTM=datetime.now(timezone.utc),
        RSLT_SUMR=summary,
        CRT_CNT=len(rows),
        FAIL_CNT=0,
    )
    db.add(history)
    db.commit()
    return history
