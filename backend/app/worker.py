"""배치 스케줄러 진입점 (로드맵 §8 "HR_AVAIL_SNAP_GEN"/"PJT_ASGN_END_ALERT" 배치 구현,
설계서 §10 자동화 배치, Phase 7 산출물 `worker.py`) — `docker-compose.yml`의 `worker`
서비스가 `python -m app.worker`로 이 모듈을 실행한다.

현재는 배치 5종(설계서 §10.1) 중 `HR_AVAIL_SNAP_GEN`(가동가능 스냅샷 생성)과
`PJT_ASGN_END_ALERT`(투입 종료 예정 알림) 2종을 구현한다 — 나머지
(`HR_DATA_QUALITY_CHK`/`PJT_WEEKLY_RPT`/`SYS_DB_BACKUP`)는 §4 Phase 7 "주요 작업" 표에
남은 순서대로 후속 작업으로 진행한다.
"""

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.session import SessionLocal
from app.services.asgn_end_alert import run_asgn_end_alert
from app.services.avail_snap_gen import run_avail_snap_gen

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("app.worker")

# 전 컨테이너가 TZ=Asia/Seoul로 통일되어 있지만(docker-compose.yml x-tz-env), 배치
# 스케줄 자체는 컨테이너 환경변수와 무관하게 항상 KST로 실행되도록 명시한다.
_KST = "Asia/Seoul"


def _job_avail_snap_gen() -> None:
    db = SessionLocal()
    try:
        history = run_avail_snap_gen(db)
        logger.info("HR_AVAIL_SNAP_GEN 완료: %s", history.RSLT_SUMR)
    except Exception:
        logger.exception("HR_AVAIL_SNAP_GEN 실행 중 오류가 발생했습니다.")
    finally:
        db.close()


def _job_asgn_end_alert() -> None:
    db = SessionLocal()
    try:
        history = run_asgn_end_alert(db)
        logger.info("PJT_ASGN_END_ALERT 완료: %s", history.RSLT_SUMR)
    except Exception:
        logger.exception("PJT_ASGN_END_ALERT 실행 중 오류가 발생했습니다.")
    finally:
        db.close()


def main() -> None:
    scheduler = BlockingScheduler(timezone=_KST)
    scheduler.add_job(
        _job_avail_snap_gen,
        CronTrigger(hour=1, minute=0, timezone=_KST),
        id="hr_avail_snap_gen",
        name="HR_AVAIL_SNAP_GEN",
        misfire_grace_time=3600,
    )
    scheduler.add_job(
        _job_asgn_end_alert,
        CronTrigger(day_of_week="fri", hour=17, minute=0, timezone=_KST),
        id="pjt_asgn_end_alert",
        name="PJT_ASGN_END_ALERT",
        misfire_grace_time=3600,
    )
    logger.info(
        "배치 스케줄러 시작 — HR_AVAIL_SNAP_GEN: 매일 01:00(KST), PJT_ASGN_END_ALERT: 매주 금 17:00(KST)"
    )
    scheduler.start()


if __name__ == "__main__":
    main()
