"""운영 DB 전환 시 `load_mock_data.py`로 넣은 목데이터만 정확히 제거하는 스크립트
(사용자 요청) — 별도의 이름 접두사 추측(`BW-`, `PJT-` 등) 방식 대신, 같은 모듈의
`EMPLOYEES`/`PROJECTS` 데이터 정의를 그대로 import해 "이 스크립트가 실제로 넣은 행"만
정확히 특정한다. 향후 실 운영 데이터가 우연히 비슷한 사번/프로젝트 코드 패턴을 쓰더라도
잘못 삭제할 위험이 없다.

부서(`HR_DEPT_MST`, 영업/세일즈파트너/딜리버리)는 이 스크립트에서 삭제하지 않는다 —
목데이터 전용이 아니라 운영에서도 그대로 사용할 조직 마스터 데이터이기 때문이다
(필요 시 별도로 정리).

**계정(`SYS_USER_MST`) 삭제 추가 (2026-07-06, 사용자 요청)**: 사원-계정 연동(§8 큐 1번)
이후 `backfill_employee_accounts.py`가 목데이터 사원에도 계정을 생성하므로, 그 계정과
`SYS_AUDIT_LOG`(로그인·계정 생성 등 이력, `USER_ID` FK) 및 감사 로그가 남아있으면
`HR_EMPL_MST` 삭제 시 FK 위반이 발생한다 — 사원을 지우기 전에 연동 계정과 그 감사
로그를 먼저 지운다. 이 스크립트 작성 이후 추가된 배치·기능이 목데이터 사원을 참조하는
테이블을 늘려서(`HR_AVAIL_SNAP_GEN` 배치의 `HR_AVAIL_SNAP`, 리소스 추천의
`PJT_RCMD_RSLT`), 실 서버에서 재검증(트랜잭션 롤백으로 안전하게 dry-run)해보니 두
테이블 모두 FK 위반으로 삭제가 막혀 있었다 — 같은 원칙으로 사원 삭제 전에 함께 제거.
프로젝트 쪽도 마찬가지로 리소스 추천 기능의 `PJT_RSRC_REQ`(요청)·`PJT_RCMD_RSLT`(결과,
`REQ_ID` 경유)가 있으면 `PJT_MST` 삭제가 막혀, 프로젝트 삭제 전에 함께 제거한다.

실행 방법 (Docker 컨테이너 내부):
    docker compose exec api python -m app.db.mock.remove_mock_data

재실행해도 안전하다 — 이미 삭제되어 없는 행은 건너뛴다.
"""

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.mock.load_mock_data import EMPLOYEES, PROJECTS
from app.db.session import SessionLocal
from app.models.hr_avail_snap import HrAvailSnap
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_role_rel import HrEmplRoleRel
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst
from app.models.pjt_rcmd_rslt import PjtRcmdRslt
from app.models.pjt_rsrc_req import PjtRsrcReq
from app.models.sys_audit_log import SysAuditLog
from app.models.sys_user_mst import SysUserMst

_MOCK_EMPL_NOS = [f"BW-{no:03d}" for no, *_ in EMPLOYEES]
_MOCK_PJT_CDS = [p["PJT_CD"] for p in PROJECTS]


def remove_mock_data(db: Session) -> dict[str, int]:
    """`load_mock_data`가 생성한 사원 30명·프로젝트 12건과 그에 딸린 역할/기술/투입
    이력·연동 계정(및 그 계정의 감사 로그)만 정확히 제거하고, 실제로 삭제한 건수를
    반환한다."""
    mock_empl_ids = list(db.scalars(select(HrEmplMst.EMPL_ID).where(HrEmplMst.EMPL_NO.in_(_MOCK_EMPL_NOS))))
    mock_pjt_ids = list(db.scalars(select(PjtMst.PJT_ID).where(PjtMst.PJT_CD.in_(_MOCK_PJT_CDS))))

    removed = {
        "assignments": 0,
        "roles": 0,
        "skills": 0,
        "avail_snaps": 0,
        "recommendation_results": 0,
        "account_audit_logs": 0,
        "accounts": 0,
        "employees": 0,
        "resource_requests": 0,
        "projects": 0,
    }

    if mock_empl_ids or mock_pjt_ids:
        result = db.execute(
            delete(PjtAsgnHis).where(
                PjtAsgnHis.EMPL_ID.in_(mock_empl_ids) | PjtAsgnHis.PJT_ID.in_(mock_pjt_ids)
            )
        )
        removed["assignments"] = result.rowcount or 0

        # 리소스 추천 결과(PJT_RCMD_RSLT)는 사원(EMPL_ID)과 요청(REQ_ID, 프로젝트 소속)
        # 양쪽에 걸려 있어 사원·프로젝트 삭제보다 먼저, 둘 중 하나라도 목데이터면 제거한다.
        mock_req_ids_stmt = select(PjtRsrcReq.REQ_ID).where(PjtRsrcReq.PJT_ID.in_(mock_pjt_ids))
        removed["recommendation_results"] = (
            db.execute(
                delete(PjtRcmdRslt).where(
                    PjtRcmdRslt.EMPL_ID.in_(mock_empl_ids) | PjtRcmdRslt.REQ_ID.in_(mock_req_ids_stmt)
                )
            ).rowcount
            or 0
        )

    if mock_empl_ids:
        removed["roles"] = (
            db.execute(delete(HrEmplRoleRel).where(HrEmplRoleRel.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )
        removed["skills"] = (
            db.execute(delete(HrEmplSkillRel).where(HrEmplSkillRel.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )
        removed["avail_snaps"] = (
            db.execute(delete(HrAvailSnap).where(HrAvailSnap.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )

        # 사원 삭제 전에 연동 계정과 그 감사 로그를 먼저 제거한다 — FK 순서:
        # SYS_AUDIT_LOG.USER_ID -> SYS_USER_MST.USER_ID -> HR_EMPL_MST.EMPL_ID
        mock_user_ids = list(
            db.scalars(select(SysUserMst.USER_ID).where(SysUserMst.EMPL_ID.in_(mock_empl_ids)))
        )
        if mock_user_ids:
            removed["account_audit_logs"] = (
                db.execute(delete(SysAuditLog).where(SysAuditLog.USER_ID.in_(mock_user_ids))).rowcount or 0
            )
            removed["accounts"] = (
                db.execute(delete(SysUserMst).where(SysUserMst.USER_ID.in_(mock_user_ids))).rowcount or 0
            )

        removed["employees"] = (
            db.execute(delete(HrEmplMst).where(HrEmplMst.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )

    if mock_pjt_ids:
        # 리소스 요청(PJT_RSRC_REQ)도 프로젝트 삭제 전에 제거해야 한다(위에서 이미
        # 그 요청에 딸린 추천 결과는 제거했으므로 순서상 안전).
        removed["resource_requests"] = (
            db.execute(delete(PjtRsrcReq).where(PjtRsrcReq.PJT_ID.in_(mock_pjt_ids))).rowcount or 0
        )
        removed["projects"] = db.execute(delete(PjtMst).where(PjtMst.PJT_ID.in_(mock_pjt_ids))).rowcount or 0

    db.commit()
    return removed


if __name__ == "__main__":
    session = SessionLocal()
    try:
        result = remove_mock_data(session)
        print(f"목데이터 제거 완료: {result}")
    finally:
        session.close()
