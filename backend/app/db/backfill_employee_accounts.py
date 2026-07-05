"""사원-계정 연동 설계 반영(§8 큐 1번, 2026-07-06) — 1-2 구현(`POST /api/v1/employees` 계정
자동 생성)은 신규 등록 사원만 다룬다. 이 스크립트는 그 기능이 추가되기 전부터 이미
`HR_EMPL_MST`에만 존재하던(연동 `SYS_USER_MST` 계정이 없는) 기존 사원을 대상으로 계정을
사후 생성하는 1회성 데이터 마이그레이션이다(운영팀 요청, 2026-07-06).

`backend/app/db/mock/`(데모용 목데이터)와 달리 이 스크립트는 실제 운영 데이터를 대상으로
하는 마이그레이션이지만, 스키마 변경이 아니라 조건에 따라 달라지는 데이터 백필이라
Alembic 마이그레이션에는 포함하지 않고(리비전 재실행 시 항상 같은 결과가 보장되어야
하는 Alembic 규칙과 맞지 않음) 독립 스크립트로 둔다 — `load_mock_data.py`와 동일한 원칙.

대상: 재직(`ACTIVE`) 또는 휴직(`LEAVE`) 상태이면서 연동 계정이 없는 사원만 포함한다.
퇴직(`RETIRED`) 사원은 계정을 새로 만들 필요가 없어 제외한다.

초기 비밀번호는 `app/core/security.py`의 `resolve_initial_password()`를 그대로 재사용한다
— `.env`의 `EMPLOYEE_INITIAL_PASSWORD`가 설정되어 있으면 그 값을, 없으면 무작위 생성값을
사용한다(사원 등록 계정 자동 생성과 동일한 정책). 이메일 발송 인프라가 없어(§9 리스크)
생성된 임시 비밀번호는 이 스크립트 실행 결과로만 확인할 수 있다 — 운영팀이 실행 즉시
출력을 확인해 각 사원에게 안전한 방법으로 직접 전달해야 한다.

재실행해도 안전하다 — 이미 계정이 연동된 사원은 건너뛴다. 이메일 중복 등으로 계정 생성이
실패한 사원은 건너뛰고 계속 진행하며, 실패 목록을 결과에 별도로 담는다(전체 롤백하지 않음
— 사원 등록 API의 "계정 생성 실패=사원 등록 실패" 원칙과 다르게, 이 스크립트는 이미 존재하는
사원 데이터를 다루므로 사원 자체를 롤백할 수 없고 계정 생성만 재시도 대상이 된다).

실행 방법 (Docker 컨테이너 내부):
    docker compose exec api python -m app.db.backfill_employee_accounts
"""

from sqlalchemy import not_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, resolve_initial_password
from app.db.session import SessionLocal
from app.models.hr_empl_mst import HrEmplMst
from app.models.sys_role_mst import SysRoleMst
from app.models.sys_user_mst import SysUserMst

_EMPLOYEE_ROLE_CD = "EMPLOYEE"
_TARGET_EMPL_STAT_CODES = ("ACTIVE", "LEAVE")


def backfill_missing_accounts(db: Session) -> dict:
    employee_role = db.scalar(select(SysRoleMst).where(SysRoleMst.ROLE_CD == _EMPLOYEE_ROLE_CD))
    if employee_role is None:
        raise RuntimeError("EMPLOYEE 역할이 SYS_ROLE_MST에 없습니다 — Seed 마이그레이션을 먼저 적용하세요.")

    linked_empl_ids_stmt = select(SysUserMst.EMPL_ID).where(SysUserMst.EMPL_ID.is_not(None))
    targets = list(
        db.scalars(
            select(HrEmplMst).where(
                HrEmplMst.EMPL_STAT_CD.in_(_TARGET_EMPL_STAT_CODES),
                not_(HrEmplMst.EMPL_ID.in_(linked_empl_ids_stmt)),
            )
        )
    )

    created: list[dict] = []
    failed: list[dict] = []
    for employee in targets:
        temp_password = resolve_initial_password()
        user = SysUserMst(
            EMPL_ID=employee.EMPL_ID,
            USER_LGID=employee.EMAIL_ADDR,
            EMAIL_ADDR=employee.EMAIL_ADDR,
            ENCR_PWD=hash_password(temp_password),
            ROLE_ID=employee_role.ROLE_ID,
            PWD_CHG_YN=True,
        )
        db.add(user)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            failed.append({"EMPL_NO": employee.EMPL_NO, "EMAIL_ADDR": employee.EMAIL_ADDR, "reason": str(exc.orig)})
            continue
        created.append(
            {
                "EMPL_NO": employee.EMPL_NO,
                "EMPL_NM": employee.EMPL_NM,
                "EMAIL_ADDR": employee.EMAIL_ADDR,
                "temp_password": temp_password,
            }
        )

    return {"created_count": len(created), "failed_count": len(failed), "created": created, "failed": failed}


if __name__ == "__main__":
    session = SessionLocal()
    try:
        result = backfill_missing_accounts(session)
        print(f"계정 백필 완료: 생성 {result['created_count']}건, 실패 {result['failed_count']}건")
        if result["created"]:
            print("\n--- 신규 생성 계정 (임시 비밀번호는 이 출력에서만 확인 가능) ---")
            for item in result["created"]:
                print(f"{item['EMPL_NO']}\t{item['EMPL_NM']}\t{item['EMAIL_ADDR']}\t{item['temp_password']}")
        if result["failed"]:
            print("\n--- 계정 생성 실패 (사번 / 이메일 / 사유) ---")
            for item in result["failed"]:
                print(f"{item['EMPL_NO']}\t{item['EMAIL_ADDR']}\t{item['reason']}")
    finally:
        session.close()
