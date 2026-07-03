# HR_JIKGUP_MST 초기 Seed (10종) — 설계서 §5.3.2 그대로 확정
# 배경: 설계서 §5.3.2에 `ResourceManagement_v2.xlsx` 드롭다운 기준 10개 직급 코드가
# 명시되어 있어(로드맵 §9 리스크 대상 아님), 이 값을 그대로 반영한다.
# `JIKGUP_ID`는 실 사용 시 Alembic Seed 스크립트에서 UUID로 생성한다 (여기서는 미포함).

HR_JIKGUP_MST_SEED = [
    {"JIKGUP_CD": "INTERN", "JIKGUP_NM": "인턴", "JIKGUP_ORD": 10},
    {"JIKGUP_CD": "SAWON", "JIKGUP_NM": "사원", "JIKGUP_ORD": 20},
    {"JIKGUP_CD": "DAERI", "JIKGUP_NM": "대리", "JIKGUP_ORD": 30},
    {"JIKGUP_CD": "CHAJANG", "JIKGUP_NM": "차장", "JIKGUP_ORD": 40},
    {"JIKGUP_CD": "BUJANG", "JIKGUP_NM": "부장", "JIKGUP_ORD": 50},
    {"JIKGUP_CD": "ISA", "JIKGUP_NM": "이사", "JIKGUP_ORD": 60},
    {"JIKGUP_CD": "SANGMUBO", "JIKGUP_NM": "상무보", "JIKGUP_ORD": 70},
    {"JIKGUP_CD": "SANGMU", "JIKGUP_NM": "상무", "JIKGUP_ORD": 80},
    {"JIKGUP_CD": "JUNMU", "JIKGUP_NM": "전무", "JIKGUP_ORD": 90},
    {"JIKGUP_CD": "BUDAEPYO", "JIKGUP_NM": "부대표", "JIKGUP_ORD": 100},
]
