from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.sys_batch_his import SysBatchHis
from app.repositories.dashboard import get_data_quality
from app.repositories.pjt_asgn_his import count_missing_end_date
from app.services.teams_notify import TeamsNotifyError, send_teams_message

BATCH_NAME = "HR_DATA_QUALITY_CHK"


def _build_message(quality: dict, missing_end_date_count: int, *, as_of: date) -> str:
    total = quality["skill_missing_count"] + quality["job_missing_count"] + quality["over_allocation_count"] + missing_end_date_count
    if total == 0:
        return f"[데이터 품질 점검] {as_of.isoformat()} 기준 이상 항목이 없습니다."

    lines = [
        f"[데이터 품질 점검] {as_of.isoformat()} 기준 이상 항목 {total}건",
        f"- 기술 미등록 인원: {quality['skill_missing_count']}명",
        f"- 직무 유형 미등록 인원: {quality['job_missing_count']}명",
        f"- 투입률 100% 초과 인원: {quality['over_allocation_count']}명",
        f"- 종료 예정일 누락 투입 건: {missing_end_date_count}건",
    ]
    return "\n".join(lines)


def run_data_quality_chk(db: Session, *, as_of: date | None = None) -> SysBatchHis:
    """`HR_DATA_QUALITY_CHK` 배치 실행기 (로드맵 §8, 설계서 §10.1 자동화 배치 — 매주
    금요일 18:00, §12.2 데이터 품질 기준). 대시보드 위젯이 이미 쓰는 `get_data_quality`
    (기술/직무 미등록·투입률 초과)를 그대로 재사용하고, 설계서 §12.2에 함께 명시된
    "종료 예정일 누락"(`count_missing_end_date`)만 이번 배치에서 신규로 추가 점검한다 —
    대시보드 API 응답 스키마(`DataQualityOut`)는 기존 3개 필드로 고정돼 있어 건드리지
    않고, 배치 요약에만 4번째 항목을 더한다.

    성공/실패 여부와 무관하게 `SYS_BATCH_HIS`에 실행 이력을 남긴다 — `PJT_ASGN_END_ALERT`
    (`app/services/asgn_end_alert.py`)와 동일한 실행/기록·Teams 알림 패턴을 따른다.
    """
    target_dt = as_of or date.today()
    started_at = datetime.now(timezone.utc)

    quality = get_data_quality(db)
    missing_end_date_count = count_missing_end_date(db)
    total_issue_count = (
        quality["skill_missing_count"] + quality["job_missing_count"] + quality["over_allocation_count"] + missing_end_date_count
    )
    message = _build_message(quality, missing_end_date_count, as_of=target_dt)

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

    summary = f"{target_dt.isoformat()} 기준 이상 항목 {total_issue_count}건 확인"
    if not sent:
        summary += " (TEAMS_WEBHOOK_URL 미설정 — 알림 전송 생략)"

    history = SysBatchHis(
        BATCH_NM=BATCH_NAME,
        EXEC_STAT_CD="SUCCESS",
        EXEC_STRT_DTTM=started_at,
        EXEC_END_DTTM=datetime.now(timezone.utc),
        RSLT_SUMR=summary,
        CRT_CNT=total_issue_count,
        FAIL_CNT=0,
    )
    db.add(history)
    db.commit()
    return history
