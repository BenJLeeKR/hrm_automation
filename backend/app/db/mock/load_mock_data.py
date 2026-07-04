"""데모/테스트용 목데이터 적재 스크립트 (사용자 요청) — `reference/ResourceManagement_v2.xlsx`의
컬럼 형식(사번 `BW-NNN`, 팀 3종, 직급 10단계, 보유역할 복수, 주요기술 쉼표 구분, 휴대폰번호
`010-0000-0000`)을 그대로 따라 사원 30명·프로젝트 12건·투입 이력을 생성한다.

`backend/app/db/seed/`(공식 마스터 Seed, Alembic 마이그레이션으로 관리)와 달리 이 스크립트는
말 그대로 데모/테스트 목적의 목데이터이므로 Alembic 마이그레이션에 포함하지 않고 독립 스크립트로
분리했다 — 스키마 변경이 아니라 언제든 재실행·삭제 가능한 트랜잭션성 예시 데이터이기 때문이다.

프로젝트 고객사명은 실제 금융회사 명칭(신한은행/KB국민은행 등)을 사용하지만, 프로젝트명·투입
내역은 전부 가상의 예시이며 실제 계약·업무 관계를 나타내지 않는다.

실행 방법 (Docker 컨테이너 내부):
    docker compose exec api python -m app.db.mock.load_mock_data

재실행해도 안전하다 — DEPT_CD/EMPL_NO/PJT_CD 기준으로 이미 존재하는 행은 건너뛴다.
"""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.hr_dept_mst import HrDeptMst
from app.models.hr_empl_mst import HrEmplMst
from app.models.hr_empl_role_rel import HrEmplRoleRel
from app.models.hr_empl_skill_rel import HrEmplSkillRel
from app.models.hr_jikgup_mst import HrJikgupMst
from app.models.hr_jikmu_mst import HrJikmuMst
from app.models.hr_skill_mst import HrSkillMst
from app.models.pjt_asgn_his import PjtAsgnHis
from app.models.pjt_mst import PjtMst

# 부서 — 엑셀 "팀" 드롭다운 3종 그대로 사용
DEPARTMENTS = [
    {"DEPT_CD": "SALES", "DEPT_NM": "영업", "DEPT_ORD": 10},
    {"DEPT_CD": "PARTNER", "DEPT_NM": "세일즈파트너", "DEPT_ORD": 20},
    {"DEPT_CD": "DELIVERY", "DEPT_NM": "딜리버리", "DEPT_ORD": 30},
]

# 사원 30명 — (사번 순번, 이름, 부서코드, 직급코드, 주 직무유형코드, 보유역할코드 목록,
#              보유기술 목록[(기술명, 숙련도)], 입사일, 휴대폰 뒤 4자리 오프셋)
EMPLOYEES = [
    (1, "김도윤", "DELIVERY", "BUJANG", "ARCHITECT", ["ARCHITECT"],
     [("시스템 아키텍처 설계", 5), ("MSA(마이크로서비스 아키텍처)", 4), ("AWS", 4)], date(2017, 3, 2)),
    (2, "이서준", "DELIVERY", "CHAJANG", "ARCHITECT", ["ARCHITECT"],
     [("시스템 아키텍처 설계", 4), ("API 설계", 4), ("Java", 4)], date(2019, 6, 1)),
    (3, "박지훈", "DELIVERY", "CHAJANG", "TECH_LEAD", ["TECH_LEAD"],
     [("Java", 5), ("Spring Boot", 4), ("API 설계", 4)], date(2018, 9, 15)),
    (4, "최민준", "DELIVERY", "CHAJANG", "TECH_LEAD", ["TECH_LEAD", "DEVOPS"],
     [("Java", 4), ("Kubernetes", 4), ("이벤트 기반 아키텍처", 3)], date(2020, 2, 3)),
    (5, "정하은", "DELIVERY", "DAERI", "DEVELOPER", ["DEVELOPER"],
     [("Java", 4), ("Spring Boot", 4), ("PostgreSQL", 3)], date(2022, 4, 1)),
    (6, "강수아", "DELIVERY", "DAERI", "DEVELOPER", ["DEVELOPER"],
     [("Java", 3), ("Spring Boot", 3), ("MyBatis", 3)], date(2022, 8, 16)),
    (7, "조은서", "DELIVERY", "SAWON", "DEVELOPER", ["DEVELOPER"],
     [("React", 4), ("TypeScript", 3), ("Next.js", 3)], date(2023, 3, 6)),
    (8, "윤재원", "DELIVERY", "SAWON", "DEVELOPER", ["DEVELOPER"],
     [("React", 3), ("JavaScript", 3), ("HTML/CSS", 3)], date(2023, 7, 10)),
    (9, "장서연", "DELIVERY", "DAERI", "DEVELOPER", ["DEVELOPER"],
     [("Python", 4), ("FastAPI", 3), ("PostgreSQL", 3)], date(2021, 11, 1)),
    (10, "임도현", "DELIVERY", "CHAJANG", "DEVELOPER", ["DEVELOPER"],
     [("Java", 5), ("Spring Boot", 5), ("Kafka", 3)], date(2016, 5, 20)),
    (11, "한지우", "DELIVERY", "SAWON", "DEVELOPER", ["DEVELOPER"],
     [("React", 3), ("Redux", 3), ("TypeScript", 3)], date(2024, 1, 15)),
    (12, "오유진", "DELIVERY", "DAERI", "DEVELOPER", ["DEVELOPER"],
     [("Java", 4), ("Spring Boot", 3), ("Oracle", 3)], date(2021, 6, 7)),
    (13, "서준혁", "DELIVERY", "DAERI", "QA", ["QA"],
     [("테스트 설계/수행", 4), ("테스트 자동화(Selenium 등)", 3), ("품질관리(QA)", 4)], date(2020, 10, 5)),
    (14, "신예은", "DELIVERY", "SAWON", "QA", ["QA"],
     [("테스트 케이스 작성", 3), ("결함관리", 3), ("품질관리(QA)", 3)], date(2023, 9, 1)),
    (15, "권민서", "DELIVERY", "CHAJANG", "DBA", ["DBA"],
     [("PostgreSQL", 5), ("Oracle", 4), ("DB 모델링/설계", 4)], date(2017, 12, 1)),
    (16, "황시우", "DELIVERY", "DAERI", "DBA", ["DBA"],
     [("PostgreSQL", 4), ("MySQL/MariaDB", 3), ("DB 모델링/설계", 3)], date(2021, 3, 15)),
    (17, "안서현", "DELIVERY", "CHAJANG", "DEVOPS", ["DEVOPS"],
     [("AWS", 4), ("Kubernetes", 4), ("Docker", 4), ("Jenkins/CI-CD", 3)], date(2019, 4, 1)),
    (18, "송지안", "DELIVERY", "DAERI", "DEVOPS", ["DEVOPS"],
     [("AWS", 3), ("Docker", 3), ("Terraform", 3)], date(2022, 5, 9)),
    (19, "전현우", "DELIVERY", "SAWON", "DESIGNER", ["DESIGNER"],
     [("HTML/CSS", 3), ("Tailwind CSS", 3)], date(2023, 11, 1)),
    (20, "홍지민", "DELIVERY", "DAERI", "DA", ["DA"],
     [("데이터 분석", 4), ("Power BI", 3), ("Tableau", 3)], date(2021, 8, 23)),
    # 21~23: 원래 "영업" 소속이었으나, "영업" 조직은 2명만 남기고 나머지는 "세일즈파트너"로
    # 이동하기로 확정(사용자 요청, 2026-07-04)해 부서코드를 PARTNER로 변경했다.
    (21, "유하준", "PARTNER", "CHAJANG", "PM", ["PM"],
     [("PMP/프로젝트관리", 5), ("일정관리", 4), ("이슈/리스크관리", 4)], date(2018, 2, 14)),
    (22, "고은채", "PARTNER", "BUJANG", "PM", ["PM"],
     [("PMP/프로젝트관리", 5), ("이슈/리스크관리", 5), ("여신업무", 3)], date(2015, 9, 1)),
    (23, "문서진", "PARTNER", "CHAJANG", "PM", ["PM"],
     [("PMP/프로젝트관리", 4), ("일정관리", 4), ("자금세탁방지(AML)", 3)], date(2019, 10, 12)),
    # "영업" 조직에 남기는 마지막 2명 — 가동률 0%(투입 없음)로 유지한다(ASSIGNMENTS 참조).
    (24, "양지호", "SALES", "BUJANG", "CONSULTANT", ["CONSULTANT"],
     [("요구사항 분석", 5), ("컨설팅 방법론", 4), ("ISP/ISMP 수립", 4)], date(2016, 6, 1)),
    (25, "손예준", "SALES", "CHAJANG", "CONSULTANT", ["CONSULTANT"],
     [("요구사항 분석", 4), ("업무 프로세스 설계(BPR)", 4), ("보험업무", 3)], date(2020, 1, 20)),
    (26, "배수빈", "PARTNER", "CHAJANG", "PMO", ["PMO"],
     [("WBS 작성", 4), ("사업관리", 4), ("품질관리(PMO)", 3)], date(2019, 7, 1)),
    (27, "백지원", "PARTNER", "DAERI", "PMO", ["PMO"],
     [("일정관리", 3), ("사업관리", 3), ("이슈/리스크관리", 3)], date(2022, 2, 8)),
    (28, "허준서", "PARTNER", "CHAJANG", "PMO", ["PMO"],
     [("WBS 작성", 4), ("품질관리(PMO)", 4), ("바젤/IFRS", 3)], date(2020, 11, 16)),
    (29, "남도윤", "PARTNER", "DAERI", "BA", ["BA"],
     [("요구사항 분석", 4), ("업무 프로세스 설계(BPR)", 3)], date(2021, 4, 5)),
    (30, "심하윤", "PARTNER", "SAWON", "BA", ["BA"],
     [("요구사항 분석", 3), ("벤치마킹/사례분석", 3)], date(2023, 5, 19)),
]

# 프로젝트 12건 — 고객사명은 실제 금융회사 명칭을 사용하되, 프로젝트명·투입 내역은 전부
# 가상의 예시이며 실제 계약·수행 내역을 나타내지 않는다.
PROJECTS = [
    {"PJT_CD": "PJT-2025-001", "PJT_NM": "차세대 코어뱅킹 구축", "CLNT_NM": "신한은행",
     # 2025년 한 해 동안 A프로젝트(연간 로테이션 시나리오 기준점) 역할을 겸하므로
     # 시작일을 2025-01-01로 앞당겼다 — 아래 ASSIGNMENTS의 2,9,18번 사원 로테이션 참조.
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2025, 1, 1), "END_DT": None},
    {"PJT_CD": "PJT-2025-002", "PJT_NM": "마이데이터 플랫폼 고도화", "CLNT_NM": "KB국민은행",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2025, 11, 1), "END_DT": None},
    {"PJT_CD": "PJT-2025-003", "PJT_NM": "디지털 채널 통합", "CLNT_NM": "하나은행",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2025, 10, 15), "END_DT": None},
    {"PJT_CD": "PJT-2026-004", "PJT_NM": "리스크관리시스템 고도화", "CLNT_NM": "우리은행",
     "PJT_STAT_CD": "PLANNED", "STRT_DT": date(2026, 9, 1), "END_DT": None},
    {"PJT_CD": "PJT-2025-005", "PJT_NM": "클라우드 전환 컨설팅", "CLNT_NM": "NH농협은행",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2025, 8, 1), "END_DT": None},
    {"PJT_CD": "PJT-2026-006", "PJT_NM": "여신심사 자동화", "CLNT_NM": "카카오뱅크",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2026, 1, 1), "END_DT": None},
    {"PJT_CD": "PJT-2025-007", "PJT_NM": "실시간 이상거래탐지(FDS) 구축", "CLNT_NM": "토스뱅크",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2025, 7, 10), "END_DT": None},
    {"PJT_CD": "PJT-2024-008", "PJT_NM": "보험금 청구 프로세스 개선", "CLNT_NM": "삼성생명",
     "PJT_STAT_CD": "CLOSED", "STRT_DT": date(2024, 3, 1), "END_DT": date(2025, 3, 31)},
    {"PJT_CD": "PJT-2025-009", "PJT_NM": "고객관리(CRM) 재구축", "CLNT_NM": "교보생명",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2025, 12, 15), "END_DT": None},
    {"PJT_CD": "PJT-2026-010", "PJT_NM": "트레이딩 플랫폼 성능개선", "CLNT_NM": "미래에셋증권",
     "PJT_STAT_CD": "PLANNED", "STRT_DT": date(2026, 10, 1), "END_DT": None},
    {"PJT_CD": "PJT-2026-011", "PJT_NM": "가맹점 정산시스템 고도화", "CLNT_NM": "신한카드",
     "PJT_STAT_CD": "RUNNING", "STRT_DT": date(2026, 2, 1), "END_DT": None},
    {"PJT_CD": "PJT-2026-012", "PJT_NM": "데이터거버넌스 체계 수립", "CLNT_NM": "현대카드",
     "PJT_STAT_CD": "HOLD", "STRT_DT": date(2026, 8, 1), "END_DT": None},
]

# 투입 이력 — (사번 순번, 프로젝트코드, 투입역할명, 투입률, 시작일, 종료일, 투입유형, 투입상태)
#
# 24·25번(영업 잔류 2명)은 의도적으로 투입 이력이 전혀 없다 — 가동률 0%(AVAILABLE) 유지.
#
# 2·9·18번은 "연간 프로젝트 로테이션" 시나리오(사용자 요청, 2026-07-04): 2025년 한 해는
# 전부 A프로젝트(PJT-2025-001, 신한은행 코어뱅킹)에 투입되었다가, 2026년부터는 각자 다른
# 프로젝트로 재배치된 것으로 조정했다(2025년 건은 ASGN_STAT_CD=DONE으로 종료 처리).
#
# 11·12·13·14번은 "복수 프로젝트 동시 투입으로 100% 초과" 시나리오(사용자 요청,
# 2026-07-04): 3~5개월간 두 프로젝트에 겹쳐 투입되어 합계 120%가 되도록 조정했다.
# 정상 등록 API(`POST /assignments`)는 100% 초과를 거부하므로, 이 초과 조합은
# API를 거치지 않고 이 스크립트에서 ORM으로 직접 생성한다 — 레거시/이관 데이터의
# 정합성 위반을 재현해 리포트의 "100% 초과 경고" 기능을 실데이터로 검증하기 위함이다.
ASSIGNMENTS = [
    (1, "PJT-2025-001", "리드 아키텍트", 100, date(2025, 9, 1), None, "RUNNING", "ACTIVE"),
    (5, "PJT-2025-001", "백엔드 개발", 100, date(2025, 9, 1), None, "RUNNING", "ACTIVE"),
    (6, "PJT-2025-001", "백엔드 개발", 100, date(2025, 9, 1), None, "RUNNING", "ACTIVE"),
    (15, "PJT-2025-001", "DB 설계", 50, date(2025, 9, 1), None, "RUNNING", "ACTIVE"),
    (3, "PJT-2025-002", "기술 리드", 100, date(2025, 11, 1), None, "RUNNING", "ACTIVE"),
    (7, "PJT-2025-002", "프론트엔드 개발", 100, date(2025, 11, 1), None, "RUNNING", "ACTIVE"),
    (8, "PJT-2025-003", "백엔드 개발", 100, date(2025, 10, 15), None, "RUNNING", "ACTIVE"),
    (19, "PJT-2025-003", "UI 설계", 100, date(2025, 10, 15), None, "RUNNING", "ACTIVE"),
    (17, "PJT-2025-005", "인프라 구축", 100, date(2025, 8, 1), None, "RUNNING", "ACTIVE"),
    (4, "PJT-2025-007", "기술 리드", 100, date(2025, 7, 10), None, "RUNNING", "ACTIVE"),
    (10, "PJT-2025-007", "백엔드 개발", 100, date(2025, 7, 10), None, "RUNNING", "ACTIVE"),
    (16, "PJT-2025-007", "DB 운영", 50, date(2025, 7, 10), None, "RUNNING", "ACTIVE"),
    (20, "PJT-2026-006", "데이터 분석", 100, date(2026, 1, 1), None, "RUNNING", "ACTIVE"),
    (29, "PJT-2026-006", "요건 분석", 100, date(2026, 1, 1), None, "RUNNING", "ACTIVE"),
    (30, "PJT-2026-011", "요건 분석", 50, date(2026, 2, 1), None, "RUNNING", "ACTIVE"),
    (21, "PJT-2026-011", "PM", 100, date(2026, 2, 1), None, "RUNNING", "ACTIVE"),
    (22, "PJT-2026-004", "PM", 100, date(2026, 9, 1), None, "COMMITTED", "PLANNED"),
    (23, "PJT-2026-010", "PM", 100, date(2026, 10, 1), None, "COMMITTED", "PLANNED"),
    (26, "PJT-2024-008", "사업관리(PMO)", 100, date(2024, 3, 1), date(2025, 3, 31), "RUNNING", "DONE"),
    (27, "PJT-2024-008", "PMO 보조", 100, date(2024, 3, 1), date(2025, 3, 31), "RUNNING", "DONE"),
    (28, "PJT-2026-012", "제안 참여(PMO)", 50, date(2026, 8, 1), None, "PROPOSED", "PLANNED"),
    # --- 연간 로테이션: 2025년 A프로젝트 → 2026년 다른 프로젝트 (2·9·18번) ---
    (2, "PJT-2025-001", "아키텍처 설계", 100, date(2025, 1, 1), date(2025, 12, 31), "RUNNING", "DONE"),
    (2, "PJT-2025-003", "아키텍처 설계", 100, date(2026, 1, 1), date(2026, 12, 31), "RUNNING", "ACTIVE"),
    (9, "PJT-2025-001", "백엔드 개발", 100, date(2025, 1, 1), date(2025, 12, 31), "RUNNING", "DONE"),
    (9, "PJT-2026-006", "백엔드 개발", 100, date(2026, 1, 1), date(2026, 12, 31), "RUNNING", "ACTIVE"),
    (18, "PJT-2025-001", "인프라 구축", 100, date(2025, 1, 1), date(2025, 12, 31), "RUNNING", "DONE"),
    (18, "PJT-2025-005", "인프라 구축", 100, date(2026, 1, 1), date(2026, 12, 31), "RUNNING", "ACTIVE"),
    # --- 복수 프로젝트 동시 투입으로 100% 초과 (11·12·13·14번, 각 3~5개월 겹침) ---
    (11, "PJT-2025-009", "프론트엔드 개발", 70, date(2026, 2, 1), date(2026, 6, 30), "RUNNING", "ACTIVE"),
    (11, "PJT-2026-011", "지원", 50, date(2026, 3, 1), date(2026, 5, 31), "RUNNING", "ACTIVE"),  # 3개월 겹침
    (12, "PJT-2025-009", "백엔드 개발", 70, date(2026, 1, 1), date(2026, 6, 30), "RUNNING", "ACTIVE"),
    (12, "PJT-2025-001", "백엔드 지원", 50, date(2026, 2, 1), date(2026, 5, 31), "RUNNING", "ACTIVE"),  # 4개월 겹침
    (13, "PJT-2025-002", "테스트", 60, date(2026, 2, 1), date(2026, 8, 31), "RUNNING", "ACTIVE"),
    (13, "PJT-2025-007", "테스트 지원", 60, date(2026, 3, 1), date(2026, 7, 31), "RUNNING", "ACTIVE"),  # 5개월 겹침
    (14, "PJT-2026-011", "품질 관리", 80, date(2026, 1, 1), date(2026, 4, 30), "RUNNING", "ACTIVE"),
    (14, "PJT-2025-005", "품질 지원", 40, date(2026, 2, 1), date(2026, 4, 30), "RUNNING", "ACTIVE"),  # 3개월 겹침
]


def _get_or_create_dept(db: Session, dept_cd: str, dept_nm: str, dept_ord: int) -> HrDeptMst:
    dept = db.scalar(select(HrDeptMst).where(HrDeptMst.DEPT_CD == dept_cd))
    if dept is None:
        dept = HrDeptMst(DEPT_CD=dept_cd, DEPT_NM=dept_nm, DEPT_ORD=dept_ord)
        db.add(dept)
        db.flush()
    return dept


def load_mock_data(db: Session) -> dict[str, int]:
    """목데이터를 적재하고 실제로 생성한 건수를 반환한다. 이미 존재하는 행(EMPL_NO/PJT_CD
    기준)은 건너뛰어 재실행해도 중복 생성되지 않는다."""
    created = {"depts": 0, "employees": 0, "roles": 0, "skills": 0, "projects": 0, "assignments": 0}

    dept_by_cd: dict[str, HrDeptMst] = {}
    for d in DEPARTMENTS:
        before = db.scalar(select(HrDeptMst).where(HrDeptMst.DEPT_CD == d["DEPT_CD"]))
        dept = _get_or_create_dept(db, d["DEPT_CD"], d["DEPT_NM"], d["DEPT_ORD"])
        dept_by_cd[d["DEPT_CD"]] = dept
        if before is None:
            created["depts"] += 1

    jikgup_by_cd = {j.JIKGUP_CD: j for j in db.scalars(select(HrJikgupMst))}
    jikmu_by_cd = {j.JIKMU_CD: j for j in db.scalars(select(HrJikmuMst))}
    skill_by_nm = {s.SKILL_NM: s for s in db.scalars(select(HrSkillMst))}

    empl_by_no: dict[str, HrEmplMst] = {}
    for no, name, dept_cd, jikgup_cd, jikmu_cd, roles, skills, hire_dt in EMPLOYEES:
        empl_no = f"BW-{no:03d}"
        existing = db.scalar(select(HrEmplMst).where(HrEmplMst.EMPL_NO == empl_no))
        if existing is not None:
            empl_by_no[empl_no] = existing
            continue

        jikmu = jikmu_by_cd.get(jikmu_cd)
        employee = HrEmplMst(
            EMPL_NO=empl_no,
            EMPL_NM=name,
            DEPT_ID=dept_by_cd[dept_cd].DEPT_ID,
            JIKGUP_ID=jikgup_by_cd[jikgup_cd].JIKGUP_ID,
            JIKMU_ID=jikmu.JIKMU_ID if jikmu else None,
            EMPL_STAT_CD="ACTIVE",
            EMAIL_ADDR=f"emp{no:03d}@blueward.co.kr",
            MPHONE_NO=f"010-2{no:03d}-{no:04d}",
            HIRE_DT=hire_dt,
        )
        db.add(employee)
        db.flush()
        empl_by_no[empl_no] = employee
        created["employees"] += 1

        for role_cd in roles:
            role_jikmu = jikmu_by_cd.get(role_cd)
            if role_jikmu is None:
                continue
            db.add(
                HrEmplRoleRel(
                    EMPL_ID=employee.EMPL_ID,
                    JIKMU_ID=role_jikmu.JIKMU_ID,
                    IS_PRIMARY=(role_cd == jikmu_cd),
                )
            )
            created["roles"] += 1

        for skill_nm, level in skills:
            skill = skill_by_nm.get(skill_nm)
            if skill is None:
                continue
            db.add(HrEmplSkillRel(EMPL_ID=employee.EMPL_ID, SKILL_ID=skill.SKILL_ID, PRFCY_LEVL=level))
            created["skills"] += 1

    pjt_by_cd: dict[str, PjtMst] = {}
    for p in PROJECTS:
        existing = db.scalar(select(PjtMst).where(PjtMst.PJT_CD == p["PJT_CD"]))
        if existing is not None:
            pjt_by_cd[p["PJT_CD"]] = existing
            continue
        project = PjtMst(
            PJT_CD=p["PJT_CD"],
            PJT_NM=p["PJT_NM"],
            CLNT_NM=p["CLNT_NM"],
            PJT_STAT_CD=p["PJT_STAT_CD"],
            STRT_DT=p["STRT_DT"],
            END_DT=p["END_DT"],
        )
        db.add(project)
        db.flush()
        pjt_by_cd[p["PJT_CD"]] = project
        created["projects"] += 1

    for no, pjt_cd, role_nm, alloc_rt, strt_dt, end_dt, asgn_type_cd, asgn_stat_cd in ASSIGNMENTS:
        empl = empl_by_no[f"BW-{no:03d}"]
        project = pjt_by_cd[pjt_cd]
        existing = db.scalar(
            select(PjtAsgnHis).where(
                PjtAsgnHis.EMPL_ID == empl.EMPL_ID,
                PjtAsgnHis.PJT_ID == project.PJT_ID,
                PjtAsgnHis.ASGN_STRT_DT == strt_dt,
            )
        )
        if existing is not None:
            continue
        db.add(
            PjtAsgnHis(
                EMPL_ID=empl.EMPL_ID,
                PJT_ID=project.PJT_ID,
                ASGN_TYPE_CD=asgn_type_cd,
                PRJT_ROLE_NM=role_nm,
                ALLOC_RT=alloc_rt,
                ASGN_STRT_DT=strt_dt,
                ASGN_END_DT=end_dt,
                ASGN_STAT_CD=asgn_stat_cd,
            )
        )
        created["assignments"] += 1

    db.commit()
    return created


if __name__ == "__main__":
    session = SessionLocal()
    try:
        result = load_mock_data(session)
        print(f"목데이터 적재 완료: {result}")
    finally:
        session.close()
