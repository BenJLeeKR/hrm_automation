# MVP 초안 — 운영팀 최종 확정 전까지 임시 데이터임.
# 배경: 로드맵 §9 리스크 "직원 기술 스택 표준화 기준 미정" 대응 초안.
#       `HR_SKILL_MST.SKILL_NM`은 설계서상 자유 입력이 금지되고 이 마스터 기준으로만
#       등록 가능하므로(설계서 §5.5 데이터 정합성 규칙), Phase 2 Alembic Seed 작성이
#       가능하도록 한국 SI/IT 조직에서 통상적으로 쓰이는 기술 스택을 우선 정리했다.
# 확정 전 주의사항:
#   1. 그룹 분류(BACKEND/FRONTEND/ARCHITECTURE/CLOUD/BUSINESS/DESIGN)와 개별 기술명은
#      운영팀 검토 후 추가/삭제/명칭 변경될 수 있다.
#   2. 실 사용 시 `SKILL_ID`는 Alembic Seed 스크립트에서 UUID로 생성한다 (여기서는 미포함).
#   3. 운영팀 확정 후 본 파일의 상단 "MVP 초안" 표기를 제거하고 로드맵 §9 리스크 항목을
#      "해결"로 갱신할 것.

HR_SKILL_MST_SEED_DRAFT = [
    # --- BACKEND ---
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Java"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Spring Boot"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Spring Framework"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Node.js"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Python"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "FastAPI"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Django"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "PHP"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Kotlin"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "C#/.NET"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Go"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "MyBatis"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "JPA/Hibernate"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Oracle"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "PostgreSQL"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "MySQL/MariaDB"},
    {"SKILL_GRP_CD": "BACKEND", "SKILL_NM": "Redis"},

    # --- FRONTEND ---
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "JavaScript"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "TypeScript"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "React"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Next.js"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Vue.js"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "Angular"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "jQuery"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "HTML/CSS"},
    {"SKILL_GRP_CD": "FRONTEND", "SKILL_NM": "전자정부표준프레임워크"},

    # --- ARCHITECTURE ---
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "시스템 아키텍처 설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "MSA(마이크로서비스 아키텍처)"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "API 설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "이벤트 기반 아키텍처"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "성능/부하 설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "DB 모델링/설계"},
    {"SKILL_GRP_CD": "ARCHITECTURE", "SKILL_NM": "보안 아키텍처"},

    # --- CLOUD ---
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "AWS"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "Azure"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "GCP"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "네이버클라우드(NCP)"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "Docker"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "Kubernetes"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "Terraform"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "Jenkins/CI-CD"},
    {"SKILL_GRP_CD": "CLOUD", "SKILL_NM": "Linux/Ubuntu 운영"},

    # --- BUSINESS ---
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "요구사항 분석"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "업무 프로세스 설계(BPR)"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "PMP/프로젝트관리"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "제안서/RFP 작성"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "SAP(ERP)"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "데이터 분석/BI"},
    {"SKILL_GRP_CD": "BUSINESS", "SKILL_NM": "IT 컨설팅"},

    # --- DESIGN ---
    {"SKILL_GRP_CD": "DESIGN", "SKILL_NM": "UI/UX 디자인"},
    {"SKILL_GRP_CD": "DESIGN", "SKILL_NM": "Figma"},
    {"SKILL_GRP_CD": "DESIGN", "SKILL_NM": "Sketch"},
    {"SKILL_GRP_CD": "DESIGN", "SKILL_NM": "Zeplin"},
    {"SKILL_GRP_CD": "DESIGN", "SKILL_NM": "프로토타이핑"},
    {"SKILL_GRP_CD": "DESIGN", "SKILL_NM": "디자인 시스템 구축"},
]
