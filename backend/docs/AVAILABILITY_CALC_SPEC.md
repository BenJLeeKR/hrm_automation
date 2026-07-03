# HRM 자동화 시스템 — 가동 가능일 MVP 산정 기준

> 출처: 설계서 `[DESIGN]HRM_Automation_System_Design_v0_6.md` §5.4의 초안 로직을 MVP 기준으로 구체화 (설계서는 수정하지 않음, 본 문서는 실행용 정리본)
> 대상: `HR_AVAIL_SNAP` 산정 로직, 배치 `HR_AVAIL_SNAP_GEN` (로드맵 §9 리스크 "가동 가능일 계산 기준 미정" 대응)
> 작성일: 2026-07-03

---

## 1. 기본 원칙

1. `HR_AVAIL_SNAP`의 가동 가능일(`AVAIL_STRT_DT`)은 **사용자가 직접 입력하지 않고 시스템이 자동 계산**한다. UI/API 모두 직접 입력을 허용하지 않는다.
2. **기준일**은 `HR_AVAIL_SNAP.SNAP_DT` (배치 실행일)로 본다. 매일 01:00 배치 `HR_AVAIL_SNAP_GEN`이 그 날짜를 기준일로 삼아 전체 사원에 대해 스냅샷을 생성한다.
3. **현재 투입률 합계**는 기준일 현재 유효한 `PJT_ASGN_HIS` 행만 집계한다 (아래 §2 산정 대상 조건 참조).

---

## 2. 산정 대상 투입 조건

기준일을 `SNAP_DT`라 할 때, 사원별 `PJT_ASGN_HIS` 중 아래 조건을 **모두** 만족하는 행만 투입률 합계 계산에 포함한다.

```sql
ASGN_STAT_CD = 'ACTIVE'
AND ASGN_STRT_DT <= SNAP_DT
AND (ASGN_END_DT IS NULL OR ASGN_END_DT >= SNAP_DT)
AND ASGN_TYPE_CD IN ('RUNNING', 'COMMITTED')
```

- `ASGN_STAT_CD`(투입 상태)가 `PLANNED`/`DONE`/`CANCELED`인 행은 제외한다.
- `ASGN_TYPE_CD = 'PROPOSED'`(제안중) 행은 **기본 가동 가능일 산정에서 제외**한다 (§3 참조).

---

## 3. `PROPOSED` 처리 — 기본 산정 제외, 대시보드/리포트 별도 표시

- `PROPOSED`(제안중) 투입은 계약이 확정되지 않은 상태이므로 `HR_AVAIL_SNAP.TOT_ALLOC_RT`/`AVAIL_STAT_CD` 산정에는 반영하지 않는다. 이는 로드맵 §4 Phase 3에서 이미 정의한 `ASGN_TYPE_CD` 3단계 가동률 집계 체계와 일치한다: `RUNNING`은 1·2·3단계 전부, `COMMITTED`는 2·3단계, `PROPOSED`는 3단계에만 포함.
- 다만 **대시보드/리포트의 "전체(+제안중)" 지표**에서는 `PROPOSED`를 포함한 투입률 합계를 별도 필드(예: `TOT_ALLOC_RT_WITH_PROPOSED`)로 함께 계산해 보여줄 수 있도록 한다. 이 값은 `HR_AVAIL_SNAP.AVAIL_STAT_CD` 산정에는 영향을 주지 않는, 참고용 3단계 집계 지표다.
- Phase 5(리소스 검색·추천), Phase 7(주간 리포트) 구현 시 이 "기본 가동률"과 "전체(+제안중) 가동률"을 화면/리포트에서 구분해 노출한다.

---

## 4. 산정 로직

기준일(`SNAP_DT`) 시점 §2 조건을 만족하는 `PJT_ASGN_HIS.ALLOC_RT` 합계를 `TOT_ALLOC_RT`라 할 때:

| `TOT_ALLOC_RT` | `AVAIL_STAT_CD` | `AVAIL_STRT_DT` |
|---|---|---|
| = 0% | `AVAILABLE` | `SNAP_DT` (기준일) |
| 1~99% | `PARTIAL` | `SNAP_DT` (기준일) |
| ≥ 100% | `FULL` | `MAX(ASGN_END_DT) + 1일` — 집계 대상 행들 중 `ASGN_END_DT` 최댓값 다음날 |
| ≥ 100%이면서 `ASGN_END_DT`가 하나라도 `NULL`인 경우 | `FULL` | `NULL`로 두고 **데이터 품질 경고 대상**으로 표시 (배치 `HR_DATA_QUALITY_CHK`에서 점검) |

의사코드:

```text
TOT_ALLOC_RT = SUM(ALLOC_RT) WHERE 위 §2 조건
IF TOT_ALLOC_RT == 0:
    AVAIL_STAT_CD = 'AVAILABLE'; AVAIL_STRT_DT = SNAP_DT
ELIF TOT_ALLOC_RT < 100:
    AVAIL_STAT_CD = 'PARTIAL'; AVAIL_STRT_DT = SNAP_DT
ELSE:  # TOT_ALLOC_RT >= 100
    IF 집계 대상 행 중 ASGN_END_DT IS NULL 인 행 존재:
        AVAIL_STAT_CD = 'FULL'; AVAIL_STRT_DT = NULL  # 데이터 품질 경고 대상
    ELSE:
        AVAIL_STAT_CD = 'FULL'; AVAIL_STRT_DT = MAX(ASGN_END_DT) + 1일
```

`AVAIL_RT`(가용률 %)는 `100 - TOT_ALLOC_RT`로 계산하되 음수가 되지 않도록 `GREATEST(0, 100 - TOT_ALLOC_RT)`로 하한을 둔다 (100% 초과분은 §5 데이터 정합성 위반 건이므로 별도 경고 대상).

---

## 5. 100% 초과 데이터 처리

- 원칙: 동일 사원의 동일 기간 `ALLOC_RT` 합계가 100%를 초과하는 것은 **저장 차단 대상**이다 (설계서 §5.5 데이터 정합성 규칙과 동일). 신규/수정 API에서는 저장 시점에 검증해 차단한다.
- 예외: **기존 Excel 이관 데이터**(Phase 8 데이터 이관분)는 이관 시점에 이미 100%를 초과해 존재할 수 있으므로 저장 차단 대상이 아니라 `HR_DATA_QUALITY_CHK` 배치의 **품질 점검 경고 대상**으로 처리한다. 이 경우 `HR_AVAIL_SNAP` 산정은 §4 로직을 그대로 적용하되(`TOT_ALLOC_RT`가 100% 초과값 그대로 집계됨), `AVAIL_RT`는 0으로 하한 처리한다.

---

## 6. 배치/서비스 구현 매핑 (참고)

| 구성 요소 | 역할 |
|---|---|
| `HR_AVAIL_SNAP_GEN` (매일 01:00 배치) | 기준일(`SNAP_DT`=실행일)로 전체 사원에 대해 §4 로직을 실행해 `HR_AVAIL_SNAP` 행 생성 |
| `availability_service.py` (Phase 5) | API 조회 시 최신 `HR_AVAIL_SNAP` 스냅샷을 기준으로 즉시 투입 가능 인력(`AVAIL_STAT_CD='AVAILABLE'`) 조회 |
| `HR_DATA_QUALITY_CHK` (매주 금요일 18:00 배치) | `AVAIL_STRT_DT IS NULL`(종료일 누락) 및 `ALLOC_RT` 100% 초과 건을 품질 경고로 집계 |

---

## 7. 운영팀 확인 필요 사항 (MVP 초안)

1. "전체(+제안중)" 지표를 대시보드/리포트 중 정확히 어느 화면·위젯에 노출할지는 Phase 5/7 화면 구현 시 확정 필요.
2. 100% 초과 이관 데이터의 경고 노출 방식(관리자 알림 vs 화면 배지 등)은 Phase 8 데이터 이관 절차 수립 시 확정 필요.
