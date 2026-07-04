from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.sys_batch_his import SysBatchHis
from app.repositories.hr_avail_snap import generate_avail_snap

BATCH_NAME = "HR_AVAIL_SNAP_GEN"


def run_avail_snap_gen(db: Session, *, snap_dt: date | None = None) -> SysBatchHis:
    """`HR_AVAIL_SNAP_GEN` 배치 실행기 (로드맵 §8, 설계서 §10 자동화 배치 — 매일 01:00
    가동가능 스냅샷 생성). 성공/실패 여부와 무관하게 `SYS_BATCH_HIS`에 실행 이력을
    남긴다 — 실패 시에도 이력이 남아야 운영팀이 배치 미실행을 감지할 수 있다.
    """
    target_dt = snap_dt or date.today()
    started_at = datetime.now(timezone.utc)

    try:
        created_count = generate_avail_snap(db, snap_dt=target_dt)
    except Exception as exc:
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

    history = SysBatchHis(
        BATCH_NM=BATCH_NAME,
        EXEC_STAT_CD="SUCCESS",
        EXEC_STRT_DTTM=started_at,
        EXEC_END_DTTM=datetime.now(timezone.utc),
        RSLT_SUMR=f"{target_dt.isoformat()} 기준 스냅샷 {created_count}건 생성",
        CRT_CNT=created_count,
        FAIL_CNT=0,
    )
    db.add(history)
    db.commit()
    return history
