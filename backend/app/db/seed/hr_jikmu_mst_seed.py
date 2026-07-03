# HR_JIKMU_MST 초기 Seed (12종) — 설계서 §5.3.3 그대로 확정
# 배경: 설계서 §5.3.3에 `ResourceManagement_v2.xlsx` "보유역할" 코드 매핑 기준 12개
# 직무 유형이 명시되어 있어(로드맵 §9 리스크 대상 아님), 이 값을 그대로 반영한다.
# 엑셀 Import 시 구 코드(AA/TA/컨설턴트/사업관리 등)를 JIKMU_CD로 매핑하는 규칙은
# 설계서 §5.3.3 및 backend/docs/ERD.md §3.3 참조.
# `JIKMU_ID`는 실 사용 시 Alembic Seed 스크립트에서 UUID로 생성한다 (여기서는 미포함).

HR_JIKMU_MST_SEED = [
    {"JIKMU_CD": "ARCHITECT", "JIKMU_NM": "아키텍트(AA)", "JIKMU_GRP_CD": "TECHNICAL"},
    {"JIKMU_CD": "TECH_LEAD", "JIKMU_NM": "기술아키텍트(TA)", "JIKMU_GRP_CD": "TECHNICAL"},
    {"JIKMU_CD": "BA", "JIKMU_NM": "비즈니스 애널리스트(BA)", "JIKMU_GRP_CD": "ANALYSIS"},
    {"JIKMU_CD": "DBA", "JIKMU_NM": "DBA", "JIKMU_GRP_CD": "TECHNICAL"},
    {"JIKMU_CD": "PM", "JIKMU_NM": "프로젝트 매니저(PM)", "JIKMU_GRP_CD": "MANAGEMENT"},
    {"JIKMU_CD": "CONSULTANT", "JIKMU_NM": "컨설턴트", "JIKMU_GRP_CD": "MANAGEMENT"},
    {"JIKMU_CD": "PMO", "JIKMU_NM": "사업관리", "JIKMU_GRP_CD": "MANAGEMENT"},
    {"JIKMU_CD": "DEVELOPER", "JIKMU_NM": "개발자", "JIKMU_GRP_CD": "TECHNICAL"},
    {"JIKMU_CD": "DA", "JIKMU_NM": "데이터 애널리스트", "JIKMU_GRP_CD": "ANALYSIS"},
    {"JIKMU_CD": "QA", "JIKMU_NM": "QA 엔지니어", "JIKMU_GRP_CD": "TECHNICAL"},
    {"JIKMU_CD": "DEVOPS", "JIKMU_NM": "DevOps/인프라", "JIKMU_GRP_CD": "TECHNICAL"},
    {"JIKMU_CD": "DESIGNER", "JIKMU_NM": "UI/UX 디자이너", "JIKMU_GRP_CD": "TECHNICAL"},
]
