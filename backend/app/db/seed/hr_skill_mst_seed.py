# `HR_SKILL_MST` 기술 마스터 표준 Seed — 한국 SI/IT 인력관리 및 IT 컨설턴트 직무 기준.
# 배경: 로드맵 §9 리스크 "직원 기술 스택 표준화 기준 미정" 대응. 기술명은 사원 목록
# Excel Import의 "주요기술" 컬럼(`employee_import.py`)과 매핑될 수 있도록 표준 영문/일반
# 명칭으로 작성했다 — `HR_SKILL_MST.SKILL_NM`은 설계서상 자유 입력이 금지되고 이 마스터
# 기준으로만 등록 가능하므로(설계서 §5.5 데이터 정합성 규칙), 최대한 실무에서 널리 쓰이는
# 표기를 우선했다.
#
# 그룹 분류(SKILL_GRP_CD) 13종 — 이전 MVP 초안(BACKEND/FRONTEND/ARCHITECTURE/CLOUD/
# BUSINESS/DESIGN 6종)을 사용자 확정 기준으로 재구성했다:
#   LANGUAGE / BACKEND / FRONTEND / MOBILE / DB / DATA / INFRA / SECURITY /
#   ARCHITECTURE / QA / CONSULTING / PMO / BUSINESS(금융 관련)
#
# 같은 (SKILL_GRP_CD, SKILL_NM) 조합이 중복 등록되지 않도록 Alembic 마이그레이션
# (`backend/alembic/versions/`, 이 모듈을 import해 재사용)에서 두 컬럼에 UNIQUE 제약을
# 추가하고 `INSERT ... ON CONFLICT DO NOTHING`으로 반영해, 이 리스트 자체를 재실행하거나
# 이미 존재하는 조합을 다시 넣어도 중복 행이 생기지 않는다.

HR_SKILL_MST_SEED = [
    # --- LANGUAGE (프로그래밍 언어) ---
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "Java"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "Python"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "JavaScript"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "TypeScript"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "Kotlin"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "C"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "C++"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "C#"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "Go"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "PHP"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "Ruby"},
    {"SKILL_GRP_CD": "LANGUAGE", "SKILL_NM": "Scala"},

    # --- BACKEND ---
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Spring Boot"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Spring Framework"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Node.js"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Express"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "NestJS"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "FastAPI"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Django"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Flask"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": ".NET"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "MyBatis"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "JPA/Hibernate"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "전자정부표준프레임워크"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "MSA(마이크로서비스 아키텍처)"},

    # --- FRONTEND ---
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "React"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Next.js"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Vue.js"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Angular"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "jQuery"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "HTML/CSS"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Redux"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Tailwind CSS"},

    # --- MOBILE ---
    {"SKILL_GRP_CD": "MOBILE", "SKILL_NM": "Android"},
    {"SKILL_GRP_CD": "MOBILE", "SKILL_NM": "iOS"},
    {"SKILL_GRP_CD": "MOBILE", "SKILL_NM": "Swift"},
    {"SKILL_GRP_CD": "MOBILE", "SKILL_NM": "Flutter"},
    {"SKILL_GRP_CD": "MOBILE", "SKILL_NM": "React Native"},
    {"SKILL_GRP_CD": "MOBILE", "SKILL_NM": "Xamarin"},

    # --- DB (데이터베이스) ---
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "Oracle"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "PostgreSQL"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "MySQL/MariaDB"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "MS-SQL"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "MongoDB"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "Redis"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "Elasticsearch"},
    {"SKILL_GRP_CD": "DB", "SKILL_NM": "DB 모델링/설계"},

    # --- DATA (데이터/분석) ---
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "데이터 분석"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "BI(Business Intelligence)"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "Tableau"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "Power BI"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "Hadoop"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "Spark"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "Kafka"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "ETL"},
    {"SKILL_GRP_CD": "DATA", "SKILL_NM": "머신러닝"},

    # --- INFRA (인프라/클라우드/운영) ---
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "AWS"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Azure"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "GCP"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "네이버클라우드(NCP)"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Docker"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Kubernetes"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Terraform"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Jenkins/CI-CD"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Linux/Unix 운영"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Nginx"},
    {"SKILL_GRP_CD": "INFRA", "SKILL_NM": "Ansible"},

    # --- SECURITY (정보보안) ---
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "정보보안 관리"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "침해대응"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "취약점 진단"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "모의해킹"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "ISMS-P"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "개인정보보호"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "암호화/PKI"},
    {"SKILL_GRP_CD": "SECURITY", "SKILL_NM": "방화벽/IPS 운영"},

    # --- ARCHITECTURE (아키텍처 설계) ---
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "시스템 아키텍처 설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "API 설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "이벤트 기반 아키텍처"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "성능/부하 설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "보안 아키텍처"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "EAI/ESB 연계 설계"},

    # --- QA (품질보증/테스트) ---
    {"SKILL_GRP_CD": "QA", "SKILL_NM": "테스트 설계/수행"},
    {"SKILL_GRP_CD": "QA", "SKILL_NM": "테스트 자동화(Selenium 등)"},
    {"SKILL_GRP_CD": "QA", "SKILL_NM": "성능 테스트"},
    {"SKILL_GRP_CD": "QA", "SKILL_NM": "품질관리(QA)"},
    {"SKILL_GRP_CD": "QA", "SKILL_NM": "결함관리"},
    {"SKILL_GRP_CD": "QA", "SKILL_NM": "테스트 케이스 작성"},

    # --- CONSULTING (IT 컨설팅) ---
    {"SKILL_GRP_CD": "CONSULTING", "SKILL_NM": "요구사항 분석"},
    {"SKILL_GRP_CD": "CONSULTING", "SKILL_NM": "업무 프로세스 설계(BPR)"},
    {"SKILL_GRP_CD": "CONSULTING", "SKILL_NM": "제안서/RFP 작성"},
    {"SKILL_GRP_CD": "CONSULTING", "SKILL_NM": "ISP/ISMP 수립"},
    {"SKILL_GRP_CD": "CONSULTING", "SKILL_NM": "컨설팅 방법론"},
    {"SKILL_GRP_CD": "CONSULTING", "SKILL_NM": "벤치마킹/사례분석"},

    # --- PMO (프로젝트 관리) ---
    {"SKILL_GRP_CD": "PMO", "SKILL_NM": "PMP/프로젝트관리"},
    {"SKILL_GRP_CD": "PMO", "SKILL_NM": "일정관리"},
    {"SKILL_GRP_CD": "PMO", "SKILL_NM": "이슈/리스크관리"},
    {"SKILL_GRP_CD": "PMO", "SKILL_NM": "품질관리(PMO)"},
    {"SKILL_GRP_CD": "PMO", "SKILL_NM": "WBS 작성"},
    {"SKILL_GRP_CD": "PMO", "SKILL_NM": "사업관리"},

    # --- BUSINESS (금융 도메인) ---
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "여신업무"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "수신업무"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "카드업무"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "보험업무"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "증권/자산운용"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "외환업무"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "전자금융"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "자금세탁방지(AML)"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "바젤/IFRS"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "SAP(ERP)"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "핀테크"},
]
