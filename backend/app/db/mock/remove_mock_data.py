"""운영 DB 전환 시 `load_mock_data.py`로 넣은 목데이터만 정확히 제거하는 스크립트
(사용자 요청) — 별도의 이름 접두사 추측(`BW-`, `PJT-` 등) 방식 대신, 같은 모듈의
`EMPLOYEES`/`PROJECTS` 데이터 정의를 그대로 import해 "이 스크립트가 실제로 넣은 행"만
정확히 특정한다. 향후 실 운영 데이터가 우연히 비슷한 사번/프로젝트 코드 패턴을 쓰더라도
잘못 삭제할 위험이 없다.

부서(`HR_DEPT_MST`, 영업/세일즈파트너/딜리버리)는 이 스크립트에서 삭제하지 않는다 —
목데이터 전용이 아니라 운영에서도 그대로 사용할 조직 마스터 데이터이기 때문이다
(필요 시 별도로 정리).

실행 방법 (Docker 컨테이너 내부):
    docker compose exec api python -m app.db.mock.remove_mock_data

재실행해도 안전하다 — 이미 삭제되어 없는 행은 건너뛴다.
"""

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.mock.load_mock_data import EMPLOYEES, PROJECTS
from app.db.session import SessionLocal
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_role_rel import HrEmplRoleRel
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst

_MOCK_EMPL_NOS = [f"BW-{no:03d}" for no, *_ in EMPLOYEES]
_MOCK_PJT_CDS = [p["PJT_CD"] for p in PROJECTS]


def remove_mock_data(db: Session) -> dict[str, int]:
    """`load_mock_data`가 생성한 사원 30명·프로젝트 12건과 그에 딸린 역할/기술/투입
    이력만 정확히 제거하고, 실제로 삭제한 건수를 반환한다."""
    mock_empl_ids = list(db.scalars(select(HrEmplMst.EMPL_ID).where(HrEmplMst.EMPL_NO.in_(_MOCK_EMPL_NOS))))
    mock_pjt_ids = list(db.scalars(select(PjtMst.PJT_ID).where(PjtMst.PJT_CD.in_(_MOCK_PJT_CDS))))

    removed = {"assignments": 0, "roles": 0, "skills": 0, "employees": 0, "projects": 0}

    if mock_empl_ids or mock_pjt_ids:
        result = db.execute(
            delete(PjtAsgnHis).where(
                PjtAsgnHis.EMPL_ID.in_(mock_empl_ids) | PjtAsgnHis.PJT_ID.in_(mock_pjt_ids)
            )
        )
        removed["assignments"] = result.rowcount or 0

    if mock_empl_ids:
        removed["roles"] = (
            db.execute(delete(HrEmplRoleRel).where(HrEmplRoleRel.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )
        removed["skills"] = (
            db.execute(delete(HrEmplSkillRel).where(HrEmplSkillRel.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )
        removed["employees"] = (
            db.execute(delete(HrEmplMst).where(HrEmplMst.EMPL_ID.in_(mock_empl_ids))).rowcount or 0
        )

    if mock_pjt_ids:
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
