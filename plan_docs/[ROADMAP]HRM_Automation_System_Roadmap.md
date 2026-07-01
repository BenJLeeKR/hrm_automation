# HRM 자동화 시스템 ROADMAP
## Roadmap v0.2

> FastAPI + PostgreSQL + Next.js + Docker 기반 구축 로드맵

**프로젝트:** Human Resource Management 자동화 시스템
**최초 작성:** 2026-07-01
**최종 수정:** 2026-07-01
**문서 버전:** v0.2
**관련 설계 문서:** `HRM_Automation_System_Design_v0.4.md`

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [상태값 정의](#2-상태값-정의)
3. [전체 개발 로드맵](#3-전체-개발-로드맵)
4. [Phase별 상세 계획](#4-phase별-상세-계획)
5. [기능별 구현 상태](#5-기능별-구현-상태)
6. [기술 구성 요소별 진행 상태](#6-기술-구성-요소별-진행-상태)
7. [개발 완료 내역](#7-개발-완료-내역)
8. [다음 작업](#8-다음-작업)
9. [리스크 및 차단 이슈](#9-리스크-및-차단-이슈)
10. [정식 운영 전환 기준](#10-정식-운영-전환-기준)
11. [MVP 구현 체크리스트](#11-mvp-구현-체크리스트)
12. [변경 이력](#12-변경-이력)

---

## 1. 프로젝트 개요

### 배경

기존 MS 365 (Excel + SharePoint + Power Automate + Power Virtual Agents) 기반으로 운영되던 리소스 관리 자동화 시스템을 독립형 웹 애플리케이션으로 전환한다.

### 구축 목표

| 항목 | 내용 |
|---|---|
| 핵심 목적 | SI/IT 조직 인력 현황·기술 스택·프로젝트 투입률·가동 가능일 통합 관리 |
| 대상 조직 규모 | 1차 기준 약 70명 / 수백 명까지 확장 가능 |
| 기준 경로 | `/App/hrmngr/` |
| DB 포트 | PostgreSQL 외부 포트 5442 (내부 5432) |
| 웹 포트 | Next.js 외부 포트 3030 |
| API 포트 | FastAPI 8000 |
| DB 명명 규칙 | 대한민국 HR 시스템 META 규칙 (`HR_*_MST`, `PJT_*_HIS`, `SYS_*`) |

### 기술 스택

| 계층 | 기술 |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 (Docker 컨테이너, 포트 5442) |
| Frontend | Next.js (포트 3030, standalone 빌드) |
| 운영 환경 | Ubuntu Server 24.04 LTS |
| 실행 환경 | Docker / Docker Compose |
| Reverse Proxy | Nginx (선택 — 운영 안정화 단계에서 추가 검토) |

---

## 2. 상태값 정의

### 개발 상태

| 상태 | 설명 |
|---|---|
| 예정 | 아직 시작하지 않은 작업 |
| 진행 중 | 현재 개발이 진행 중인 작업 |
| 완료 | 개발·검증이 완료된 작업 |
| 보류 | 일시적으로 중단된 작업 (재개 예정) |
| 제외 | 범위에서 제외된 작업 (해당 Phase에서 수행하지 않음) |

### 일정 상태

| 상태 | 설명 |
|---|---|
| 정상 | 계획 일정 내 진행 중 |
| 주의 | 지연 가능성이 있어 모니터링 필요 |
| 지연 | 계획 일정을 초과한 상태 |
| 차단 | 선행 조건 미충족으로 진행 불가 |

### 우선순위

| 우선순위 | 설명 |
|---|---|
| 높음 | MVP 필수 기능 — 이 없으면 운영 불가 |
| 중간 | 운영에 필요하지만 대안이 있는 기능 |
| 낮음 | 편의 기능 또는 확장 기능 |

---

## 3. 전체 개발 로드맵

| Phase | 이름 | 계획 기간 | 개발 상태 | 진행률 | 일정 상태 |
|---|---|---|---|---:|---|
| Phase 0 | 프로젝트 기반 정리 | 1주차 | 완료 | 100% | 정상 |
| Phase 1 | 인프라 및 개발환경 구축 | 2주차 | 예정 | 0% | 정상 |
| Phase 2 | PostgreSQL 데이터 모델 구축 | 2~3주차 | 예정 | 0% | 정상 |
| Phase 3 | FastAPI 백엔드 구축 | 3~5주차 | 예정 | 0% | 정상 |
| Phase 4 | Next.js 웹 클라이언트 구축 | 3~5주차 | 예정 | 0% | 정상 |
| Phase 5 | 리소스 검색 및 추천 기능 구축 | 5주차 | 예정 | 0% | 정상 |
| Phase 6 | AI 질의응답 연동 | 7주차 | 예정 | 0% | 정상 |
| Phase 7 | 운영 자동화 및 배포 안정화 | 6~7주차 | 예정 | 0% | 정상 |
| Phase 8 | 파일럿 운영 및 정식 전환 | 8주차 | 예정 | 0% | 정상 |

---

## 4. Phase별 상세 계획

---

### Phase 0. 프로젝트 기반 정리

| 항목 | 내용 |
|---|---|
| **목표** | 기존 MS 365 기반 설계를 폐기하고, FastAPI + PostgreSQL + Next.js + Docker 기반 아키텍처로 전환 확정 |
| **계획 기간** | 1주차 |
| **개발 상태** | 완료 |
| **진행률** | 100% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| 기존 MS 365 기반 설계 분석 및 한계 정리 | 완료 |
| 신규 기술 스택 확정 (FastAPI + PostgreSQL + Next.js + Docker) | 완료 |
| 프로젝트 기준 경로 확정 (`/App/hrmngr/`) | 완료 |
| 포트 정책 확정 (Web 3030, API 8000, DB 5442) | 완료 |
| DB META 명명 규칙 확정 (한국 HR 시스템 규칙) | 완료 |
| 직무 유형(`HR_JIKMU_MST`) 도입 결정 | 완료 |
| 설계 문서 v0.4 작성 완료 | 완료 |
| Nginx 구성 분리 (초기 제외, 운영 단계 선택) | 완료 |

**산출물**

- `HRM_Automation_System_Design_v0.4.md` (설계 문서)
- `ROADMAP.md` (본 문서)

**완료 기준**

- 기술 스택·DB 명명 규칙·포트 정책·디렉토리 구조가 설계 문서에 확정 기재됨
- 팀원 공유 및 리뷰 완료

---

### Phase 1. 인프라 및 개발환경 구축

| 항목 | 내용 |
|---|---|
| **목표** | Docker 기반 개발·운영 환경 구성 및 전체 서비스 컨테이너 기동 확인 |
| **계획 기간** | 2주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| Ubuntu Server 24.04 LTS 환경 준비 | 예정 |
| Docker Engine 설치 | 예정 |
| Docker Compose Plugin 설치 | 예정 |
| `/App/hrmngr/` 디렉토리 구조 생성 | 예정 |
| `docker-compose.yml` 초안 작성 (api / web / db / redis / worker) | 예정 |
| `.env` 파일 작성 및 `.gitignore` 설정 | 예정 |
| Git Repository 초기화 | 예정 |
| PostgreSQL 컨테이너 기동 및 포트 5442 접속 확인 | 예정 |
| FastAPI 컨테이너 기동 및 `/health` 응답 확인 | 예정 |
| Next.js 컨테이너 기동 및 포트 3030 접속 확인 | 예정 |
| 방화벽(UFW) 설정 (3030, 8000 허용 / 5442 내부망 제한) | 예정 |

**산출물**

- `docker-compose.yml`
- `.env.example`
- `.gitignore`
- `README.md` (기동 명령어 포함)

**완료 기준**

- `docker compose up -d` 한 번으로 api / web / db / redis / worker 5개 컨테이너 모두 정상 기동
- `http://{서버IP}:3030` Next.js 초기 화면 접근 가능
- `http://{서버IP}:8000/health` FastAPI 헬스체크 응답 확인
- `localhost:5442` PostgreSQL 외부 접속 확인 (DBeaver 등)

---

### Phase 2. PostgreSQL 데이터 모델 구축

| 항목 | 내용 |
|---|---|
| **목표** | 한국 HR META 명명 규칙 기반 전체 테이블 생성 및 초기 데이터 적재 |
| **계획 기간** | 2~3주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| ERD 최종 확정 | 예정 |
| Alembic 마이그레이션 환경 구성 | 예정 |
| `HR_DEPT_MST` (부서 마스터) 테이블 생성 | 예정 |
| `HR_JIKGUP_MST` (직급 마스터) 테이블 생성 | 예정 |
| `HR_JIKMU_MST` (직무 마스터) 테이블 생성 | 예정 |
| `HR_SKILL_MST` (기술 마스터) 테이블 생성 | 예정 |
| `HR_EMPL_MST` (사원 마스터) 테이블 생성 | 예정 |
| `HR_EMPL_SKILL_REL` (사원기술 연결) 테이블 생성 | 예정 |
| `PJT_MST` (프로젝트 마스터) 테이블 생성 | 예정 |
| `PJT_ASGN_HIS` (투입 이력) 테이블 생성 | 예정 |
| `PJT_RSRC_REQ` (리소스 요청) 테이블 생성 | 예정 |
| `PJT_RCMD_RSLT` (추천 결과) 테이블 생성 | 예정 |
| `HR_AVAIL_SNAP` (가동가능 스냅샷) 테이블 생성 | 예정 |
| `SYS_USER_MST` (사용자 마스터) 테이블 생성 | 예정 |
| `SYS_ROLE_MST` (역할 마스터) 테이블 생성 | 예정 |
| `SYS_AUDIT_LOG` (감사 로그) 테이블 생성 | 예정 |
| `SYS_BATCH_HIS` (배치 이력) 테이블 생성 | 예정 |
| Seed 데이터 입력 (`SYS_ROLE_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST` 12종) | 예정 |
| DB 백업 스크립트 작성 및 crontab 등록 (매일 02:00) | 예정 |

**산출물**

- Alembic 마이그레이션 스크립트 (전체 테이블)
- Seed 데이터 SQL 또는 Python 스크립트
- `backup_db.sh`

**완료 기준**

- `alembic upgrade head` 실행 후 15개 테이블 전부 생성 확인
- Seed 데이터 정상 입력 확인
- `pg_dump` 백업 파일 생성 확인

---

### Phase 3. FastAPI 백엔드 구축

| 항목 | 내용 |
|---|---|
| **목표** | 핵심 업무 도메인 REST API 구현 및 인증·권한·감사 로그 적용 |
| **계획 기간** | 3~5주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| FastAPI 프로젝트 기본 구조 생성 (`app/`, `models/`, `schemas/`, `api/v1/`) | 예정 |
| SQLAlchemy 2.x ORM 모델 작성 (15개 테이블) | 예정 |
| Pydantic v2 스키마 작성 | 예정 |
| `/health` 헬스체크 엔드포인트 구현 | 예정 |
| JWT 인증 API 구현 (`SYS_USER_MST` 기반) | 예정 |
| RBAC 권한 미들웨어 구현 (`SYS_ROLE_MST` 기반) | 예정 |
| `SYS_AUDIT_LOG` 감사 로그 미들웨어 구현 | 예정 |
| CORS 설정 (포트 3030 허용) | 예정 |
| 사원 CRUD API (`HR_EMPL_MST`) | 예정 |
| 부서/직급/직무 코드 API (`HR_DEPT_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST`) | 예정 |
| 기술 CRUD API (`HR_SKILL_MST`, `HR_EMPL_SKILL_REL`) | 예정 |
| 프로젝트 CRUD API (`PJT_MST`) | 예정 |
| 투입 관리 API (`PJT_ASGN_HIS`) | 예정 |
| 가동률 계산 API (`HR_AVAIL_SNAP`) | 예정 |
| 대시보드 집계 API | 예정 |
| Excel Import/Export API | 예정 |
| 페이지네이션 공통 처리 구현 | 예정 |
| OpenAPI 문서 확인 (`/docs`) | 예정 |

**산출물**

- FastAPI 앱 전체 소스 (`/App/hrmngr/backend/`)
- OpenAPI 문서 (`/docs`, `/redoc`)

**완료 기준**

- 핵심 CRUD 엔드포인트 전부 응답 확인 (Postman 또는 `/docs` 기준)
- JWT 인증·RBAC 권한 필터 동작 확인
- `SYS_AUDIT_LOG` 변경 이력 기록 확인
- Pytest 단위 테스트 핵심 API 커버

---

### Phase 4. Next.js 웹 클라이언트 구축

| 항목 | 내용 |
|---|---|
| **목표** | 권한별 메뉴 제어가 적용된 웹 화면 전체 구현 (포트 3030) |
| **계획 기간** | 3~5주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| Next.js 프로젝트 생성 (`output: 'standalone'`) | 예정 |
| `NEXT_PUBLIC_API_BASE_URL` 환경변수 설정 | 예정 |
| 로그인 화면 구현 (`/login`) | 예정 |
| 공통 레이아웃·네비게이션 구현 (권한별 메뉴 제어) | 예정 |
| 대시보드 화면 구현 (`/dashboard`) — 직무 유형 분포 위젯 포함 | 예정 |
| 사원 목록 화면 구현 (`/employees`) — 직무 유형 필터 포함 | 예정 |
| 사원 상세 화면 구현 (`/employees/[id]`) | 예정 |
| 기술 관리 화면 구현 (`/skills`) | 예정 |
| 직무 유형 관리 화면 구현 (`/job-types`) | 예정 |
| 프로젝트 목록/상세 화면 구현 (`/projects`, `/projects/[id]`) | 예정 |
| 투입 관리 화면 구현 (`/assignments`) | 예정 |
| 가동 가능 인력 조회 화면 구현 (`/availability`) | 예정 |
| 리포트 화면 구현 (`/reports`) | 예정 |
| 설정 화면 구현 (`/settings/users`, `/settings/audit-logs`) | 예정 |
| Excel Import/Export UI 구현 | 예정 |

**산출물**

- Next.js 앱 전체 소스 (`/App/hrmngr/frontend/`)
- 화면별 컴포넌트

**완료 기준**

- 전체 화면 브라우저에서 정상 렌더링 확인
- 로그인 → 권한별 메뉴 노출 확인
- API 연동 (사원 목록·프로젝트 목록·대시보드 데이터) 정상 동작 확인

---

### Phase 5. 리소스 검색 및 추천 기능 구축

| 항목 | 내용 |
|---|---|
| **목표** | 직무 유형·기술·가동 가능일 기반 인력 검색 및 점수 기반 추천 구현 |
| **계획 기간** | 5주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| 가동 가능일 자동 계산 로직 구현 (`HR_AVAIL_SNAP` 기반) | 예정 |
| 즉시 투입 가능 인력 조회 API 구현 | 예정 |
| 직무 유형·기술·숙련도 복합 필터 검색 API 구현 | 예정 |
| 추천 점수 산정 로직 구현 (직무 일치 15% + 기술 35% + 숙련도 25% + 가동일 15% + 경험 10%) | 예정 |
| `PJT_RSRC_REQ` 인력 요청 등록 API 구현 | 예정 |
| `PJT_RCMD_RSLT` 추천 결과 저장 및 조회 API 구현 | 예정 |
| 리소스 추천 화면 구현 (`/recommendations`) — 직무 유형 조건 포함 | 예정 |
| 가동 가능 인력 화면 구현 (`/availability`) | 예정 |

**산출물**

- `recommendation_service.py`
- `availability_service.py`
- `/recommendations` 화면

**완료 기준**

- 직무 유형 + 기술 + 가동 가능일 조건 복합 검색 결과 정확성 확인
- 추천 점수 기준으로 정렬된 후보 목록 반환 확인
- `PJT_RCMD_RSLT` 테이블에 추천 결과 저장 확인

---

### Phase 6. AI 질의응답 연동

| 항목 | 내용 |
|---|---|
| **목표** | LLM API 기반 자연어 인력 검색·추천 기능 구현 (SQL 조회 기반, 권한 필터 적용) |
| **계획 기간** | 7주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| LLM 연동 인터페이스 추상화 (멀티 LLM 전환 가능 구조) | 예정 |
| 자연어 조건 파싱 구현 (`JIKMU_CD`, `SKILL_NM`, 가동일 인식) | 예정 |
| 파싱 결과 → SQL 조회 → 결과 요약 흐름 구현 | 예정 |
| 권한 필터링 후 LLM 컨텍스트 전달 구현 | 예정 |
| 환각 방지 시스템 프롬프트 적용 | 예정 |
| `POST /api/v1/ai/chat` 엔드포인트 구현 | 예정 |
| AI Chat 화면 구현 (`/ai-chat`) | 예정 |
| 테스트 질의 10개 이상 검증 (직무 유형 포함) | 예정 |

**산출물**

- `ai_service.py`
- `/ai-chat` 화면

**완료 기준**

- "다음 달 투입 가능한 Java 아키텍트" 등 자연어 질의에 정확한 후보 반환
- `SYS_AUDIT_LOG`에 AI 질의 이력 기록
- 권한 없는 정보 미노출 확인

---

### Phase 7. 운영 자동화 및 배포 안정화

| 항목 | 내용 |
|---|---|
| **목표** | 배치 스케줄러·알림·로그·백업 자동화 완성 및 운영 환경 안정화 |
| **계획 기간** | 6~7주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| `HR_AVAIL_SNAP_GEN` 배치 구현 (매일 01:00 가동가능 스냅샷 생성) | 예정 |
| `PJT_ASGN_END_ALERT` 배치 구현 (매주 금요일 17:00 종료 예정 알림) | 예정 |
| `HR_DATA_QUALITY_CHK` 배치 구현 (매주 금요일 18:00 데이터 품질 점검) | 예정 |
| `PJT_WEEKLY_RPT` 배치 구현 (매주 월요일 09:00 주간 리포트 발송) | 예정 |
| `SYS_DB_BACKUP` 배치 구현 (매일 02:00, crontab 등록) | 예정 |
| Teams Webhook 알림 연동 | 예정 |
| 구조화 로그(JSON) 설정 | 예정 |
| Docker 컨테이너 재기동 절차 문서화 | 예정 |
| `restart: unless-stopped` 자동 재기동 설정 확인 | 예정 |
| Nginx 도입 여부 재검토 (HTTPS/도메인 필요 시) | 예정 |

**산출물**

- `worker.py` (APScheduler 기반 배치)
- `report_service.py`
- 운영 가이드 문서

**완료 기준**

- 배치 5종 정상 실행 확인 (`SYS_BATCH_HIS` 기록 확인)
- Teams 알림 수신 확인
- 서버 재시작 후 모든 컨테이너 자동 복구 확인
- `pg_dump` 백업 파일 `/App/hrmngr/backup/postgres/`에 정상 생성

---

### Phase 8. 파일럿 운영 및 정식 전환

| 항목 | 내용 |
|---|---|
| **목표** | 실제 사용자 파일럿 테스트 완료 후 Excel 중심 운영에서 시스템 중심 운영으로 전환 |
| **계획 기간** | 8주차 |
| **개발 상태** | 예정 |
| **진행률** | 0% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| 기존 Excel 데이터 `HR_EMPL_MST` 등으로 일괄 이관 | 예정 |
| `HR_EMPL_MST.JIKMU_ID` 직무 유형 수동 보정 | 예정 |
| 파일럿 사용자 계정 생성 (`SYS_USER_MST`) | 예정 |
| 파일럿 사용자 테스트 수행 (PM·운영팀장·팀장 역할) | 예정 |
| 오류 수집 및 수정 | 예정 |
| 정식 운영 전환 기준 항목 최종 점검 | 예정 |
| 전사 공지 및 사용자 교육 | 예정 |
| 정식 운영 선언 | 예정 |

**산출물**

- 이관 완료 데이터
- 파일럿 테스트 결과 리포트
- 사용자 교육 자료

**완료 기준**

- 정식 운영 전환 기준 10개 항목 전부 충족 (10. 정식 운영 전환 기준 참조)
- 주요 오류 없이 2주 이상 운영

---

## 5. 기능별 구현 상태

| 기능 영역 | 주요 기능 | 상태 | 우선순위 | 관련 모듈 | 비고 |
|---|---|---|---|---|---|
| 직원 관리 | `HR_EMPL_MST` CRUD, 퇴직 처리 | 예정 | 높음 | `employees.py`, `HR_EMPL_MST` | 직무 유형(`JIKMU_ID`) 필드 포함 |
| 팀/조직 관리 | `HR_DEPT_MST` 계층 구조 관리 | 예정 | 높음 | `departments.py`, `HR_DEPT_MST` | 상위 부서(`PRNT_DEPT_ID`) 지원 |
| 직급/역할 관리 | `HR_JIKGUP_MST`, `HR_JIKMU_MST` 마스터 관리 | 예정 | 높음 | `positions.py`, `job_types.py` | 직급·직무 분리 설계 |
| 기술 스택 관리 | `HR_SKILL_MST` CRUD | 예정 | 높음 | `skills.py`, `HR_SKILL_MST` | 기술 그룹(`SKILL_GRP_CD`) 분류 |
| 직원별 숙련도 관리 | `HR_EMPL_SKILL_REL` 등록·수정 | 예정 | 높음 | `employees.py`, `HR_EMPL_SKILL_REL` | `PRFCY_LEVL` 1~5 |
| 프로젝트 관리 | `PJT_MST` CRUD, 상태 관리 | 예정 | 높음 | `projects.py`, `PJT_MST` | `PJT_STAT_CD` (PLANNED/RUNNING/CLOSED/HOLD) |
| 프로젝트 투입 관리 | `PJT_ASGN_HIS` 등록·수정·취소 | 예정 | 높음 | `assignments.py`, `PJT_ASGN_HIS` | 투입 역할(`PRJT_ROLE_NM`) 포함 |
| 투입률 관리 | `ALLOC_RT` 합계 검증 및 표시 | 예정 | 높음 | `availability_service.py` | 동일 기간 합계 100% 초과 방지 |
| 종료 예정일 관리 | `ASGN_END_DT` 조회·알림 | 예정 | 높음 | `PJT_ASGN_HIS`, `PJT_ASGN_END_ALERT` 배치 | 30일 이내 종료 예정 알림 |
| 가동 가능일 자동 계산 | `HR_AVAIL_SNAP` 기반 산정 | 예정 | 높음 | `availability_service.py`, `HR_AVAIL_SNAP_GEN` 배치 | 투입률 0%=오늘, <100%=부분, ≥100%=MAX(종료일)+1 |
| 즉시 투입 가능 인력 조회 | `AVAIL_STAT_CD='AVAILABLE'` 필터 | 예정 | 높음 | `GET /api/v1/availability` | 직무 유형 필터 포함 |
| 기술 기반 인력 검색 | 기술·숙련도·직무 복합 검색 | 예정 | 높음 | `recommendations.py` | `HR_EMPL_SKILL_REL` + `HR_JIKMU_MST` 조인 |
| 프로젝트 종료 예정자 조회 | 이번 달/30일 이내 종료 예정자 | 예정 | 높음 | `reports.py`, `PJT_ASGN_HIS` | |
| 팀별 가동률 조회 | 부서별 평균 `TOT_ALLOC_RT` | 예정 | 중간 | `dashboard.py`, `HR_AVAIL_SNAP` | |
| 리소스 추천 | `PJT_RCMD_RSLT` 점수 기반 후보 추천 | 예정 | 중간 | `recommendation_service.py` | 6개 항목 가중 점수 |
| AI 질의응답 | 자연어 → 조건 파싱 → SQL 조회 → 요약 | 예정 | 중간 | `ai_service.py`, `POST /api/v1/ai/chat` | Phase 6 |
| 주간 리포트 | `PJT_WEEKLY_RPT` 자동 발송 | 예정 | 중간 | `report_service.py`, Teams Webhook | 매주 월요일 09:00 |
| 감사 로그 | `SYS_AUDIT_LOG` 변경 이력 기록 | 예정 | 높음 | `sys_audit_log.py`, 미들웨어 | 로그인·CRUD·Import 포함 |
| 사용자 인증/권한 | JWT + RBAC (`SYS_USER_MST`, `SYS_ROLE_MST`) | 예정 | 높음 | `auth.py`, `security.py` | 6개 역할 |
| 백업/복구 | `SYS_DB_BACKUP` 자동화, `pg_dump` | 예정 | 높음 | `backup_db.sh`, crontab | 매일 02:00, 14일 보관 |
| 배포 자동화 | Docker Compose 기반 배포 | 예정 | 높음 | `docker-compose.yml` | CI/CD는 확장 단계 |

---

## 6. 기술 구성 요소별 진행 상태

| 구성 요소 | 적용 기술 | 상태 | 필수 여부 | 비고 |
|---|---|---|---|---|
| Ubuntu Server | Ubuntu 24.04 LTS | 예정 | 필수 | 운영 서버 OS |
| Docker | Docker Engine (최신) | 예정 | 필수 | 컨테이너 런타임 |
| Docker Compose | Docker Compose Plugin v2 | 예정 | 필수 | 멀티 컨테이너 오케스트레이션 |
| PostgreSQL | PostgreSQL 16-alpine (Docker) | 예정 | 필수 | 외부 포트 5442, 데이터 `/App/hrmngr/data/postgres/` |
| FastAPI | FastAPI + Uvicorn (Python 3.12) | 예정 | 필수 | 포트 8000, 운영 시 Gunicorn+Uvicorn Worker 전환 검토 |
| SQLAlchemy 또는 SQLModel | SQLAlchemy 2.x + Alembic | 예정 | 필수 | ORM 및 마이그레이션 |
| Alembic | Alembic (SQLAlchemy 연동) | 예정 | 필수 | DB 스키마 버전 관리 |
| Next.js | Next.js (node:22-alpine, standalone) | 예정 | 필수 | 외부 포트 3030, `output: 'standalone'` |
| API Client | Axios 또는 fetch (Next.js 내장) | 예정 | 필수 | `NEXT_PUBLIC_API_BASE_URL` 환경변수 기반 |
| 인증 방식 | JWT (Access Token 60분 + Refresh Token 7일) | 예정 | 필수 | HttpOnly Cookie, Token Rotation |
| Batch/Scheduler | APScheduler (MVP) → Celery (확장) | 예정 | 필수 | `hrm-worker` 컨테이너 |
| Logging | structlog 또는 Python logging (JSON 포맷) | 예정 | 필수 | `/App/hrmngr/logs/` |
| Backup | `pg_dump` + gzip + crontab | 예정 | 필수 | `/App/hrmngr/backup/postgres/`, 14일 보관 |
| Nginx | Nginx (선택) | 예정 | 선택 | 초기 구축에서는 제외 가능하며, HTTPS/도메인/운영 안정화 단계에서 추가 검토 |
| AI Agent / LLM 연동 | OpenAI API 또는 Anthropic API (MVP), 사내 LLM (확장) | 예정 | 선택 | Phase 6, LLM 호출 레이어 추상화 필수 |
| Redis | Redis 7-alpine (Docker) | 예정 | 선택 | 캐시·비동기 큐, MVP에서 생략 가능 |

---

## 7. 개발 완료 내역

### 2026-07-01

- 기존 MS 365 중심 설계 (Excel + SharePoint + Power Automate + PVA)를 FastAPI + PostgreSQL + Next.js + Docker 기반 구조로 전환 확정
- PostgreSQL을 HRM 시스템의 중심 저장소(Single Source of Truth)로 설정
- Excel/SharePoint는 초기 데이터 마이그레이션 또는 보조 입력 수단으로만 활용 가능하도록 역할 조정
- Nginx는 초기 필수 구성요소가 아니라 운영 확장 선택사항으로 분리 (HTTPS/도메인 필요 시 Phase 7에서 검토)
- 직원, 기술 스택, 프로젝트, 투입률, 종료 예정일, 가동 가능일을 핵심 관리 대상으로 정의
- DB 테이블명·컬럼명을 대한민국 HR 시스템 META 명명 규칙으로 전면 재정의 (`HR_EMPL_MST`, `PJT_ASGN_HIS`, `SYS_AUDIT_LOG` 등)
- 직무 유형 마스터(`HR_JIKMU_MST`) 도입 — 아키텍트/개발자/BA 등 12종 Seed 데이터 정의
- 포트 정책 확정: Next.js 3030, FastAPI 8000, PostgreSQL 5442
- 프로젝트 기준 경로 확정: `/App/hrmngr/`
- 설계 문서 `HRM_Automation_System_Design_v0.4.md` 작성 완료
- `ROADMAP.md` 최초 작성 완료 (본 문서)

---

## 8. 다음 작업

> 개발자가 Phase 1~2 시작 시 즉시 수행할 수 있는 작업 단위.
> 순서대로 수행하는 것을 권장한다.

- [ ] 1. PostgreSQL ERD 최종 확정 (`HR_EMPL_MST` 등 15개 테이블 관계 검토)
- [ ] 2. Docker Compose 개발환경 구성 (`docker-compose.yml` 작성 — api / web / db / redis / worker)
- [ ] 3. FastAPI 프로젝트 기본 구조 생성 (`app/`, `models/`, `schemas/`, `api/v1/`, `core/`)
- [ ] 4. PostgreSQL 초기 마이그레이션 구성 (Alembic `env.py` 설정)
- [ ] 5. `HR_DEPT_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST`, `HR_SKILL_MST`, `HR_EMPL_MST`, `PJT_MST`, `PJT_ASGN_HIS` 테이블 생성
- [ ] 6. `SYS_USER_MST`, `SYS_ROLE_MST`, `SYS_AUDIT_LOG` 테이블 생성 및 Seed 데이터 입력
- [ ] 7. 사원 목록 조회 API 구현 (`GET /api/v1/employees`)
- [ ] 8. 사원 등록/수정 API 구현 (`POST`, `PATCH /api/v1/employees`)
- [ ] 9. Next.js 기본 레이아웃 구성 (로그인 화면, 공통 네비게이션)
- [ ] 10. 사원 목록 화면 구현 (`/employees` — 직무 유형 필터 포함)
- [ ] 11. 프로젝트 투입 현황 화면 구현 (`/assignments`)

---

## 9. 리스크 및 차단 이슈

| 이슈 | 영향도 | 상태 | 대응 방안 |
|---|---|---|---|
| 직원 기술 스택 표준화 기준 미정 | 높음 | 차단 | `HR_SKILL_MST` 마스터 초안 작성 후 운영팀 확정 필요 — Phase 2 시작 전 완료 목표 |
| 가동 가능일 계산 기준 미정 | 높음 | 차단 | `HR_AVAIL_SNAP` 산정 로직 (투입률 0%=오늘, <100%=부분, ≥100%=MAX 종료일+1) 초안 확정 후 관계자 검토 필요 |
| 인증/권한 범위 미정 | 높음 | 차단 | `SYS_ROLE_MST` 6개 역할(Admin/HR_MGR/PM/TEAM_LEAD/EXEC/VIEWER) 및 기능별 권한 매트릭스 관계자 승인 필요 |
| AI 질의응답 연동 범위 미정 | 중간 | 주의 | MVP는 OpenAI/Anthropic API 연동, 보안 요건에 따라 사내 LLM 전환 — Phase 5 완료 후 결정 |
| 기존 Excel/SharePoint 데이터 마이그레이션 방식 미정 | 높음 | 주의 | Excel Import 기능 구현 (Phase 3) 후 데이터 정제 절차 수립 — Phase 8 전 완료 목표 |
| 운영 서버 백업 정책 미정 | 중간 | 주의 | `pg_dump` 매일 02:00 + 14일 보관 + 외부 스토리지 복제 초안 제시, 운영팀 확인 필요 |
| 서버 HTTPS/도메인 미적용 | 낮음 | 주의 | 초기 구축은 내부망 HTTP로 운영, Phase 7에서 Nginx + TLS 도입 여부 재검토 |
| `HR_EMPL_MST.JIKMU_ID` 기존 데이터 없음 | 낮음 | 주의 | NULL 허용 설계로 이관 후 운영팀 수동 보정, Phase 8 데이터 이관 시 처리 |

---

## 10. 정식 운영 전환 기준

정식 운영 전환은 아래 항목이 **전부** 충족되었을 때 선언한다.

| # | 기준 항목 | 충족 여부 |
|---:|---|---|
| 1 | `HR_EMPL_MST` 기반 직원 기본 정보 등록/수정/조회 가능 | 미충족 |
| 2 | `PJT_MST` + `PJT_ASGN_HIS` 기반 프로젝트 및 투입률 관리 가능 | 미충족 |
| 3 | `HR_SKILL_MST` + `HR_EMPL_SKILL_REL` 기반 기술 인력 검색 가능 | 미충족 |
| 4 | `HR_AVAIL_SNAP.AVAIL_STAT_CD='AVAILABLE'` 기준 즉시 투입 가능 인력 조회 가능 | 미충족 |
| 5 | `HR_AVAIL_SNAP` 가동 가능일 자동 계산 가능 (배치 `HR_AVAIL_SNAP_GEN` 정상 동작) | 미충족 |
| 6 | `SYS_ROLE_MST` 기반 관리자 권한 기준 적용 (RBAC 동작 확인) | 미충족 |
| 7 | `SYS_DB_BACKUP` 배치 기반 PostgreSQL 데이터 자동 백업 절차 수립 및 복구 테스트 완료 | 미충족 |
| 8 | Docker Compose 재기동 절차 문서화 및 검증 완료 | 미충족 |
| 9 | 파일럿 사용자(PM·운영팀장·팀장) 테스트 완료 및 주요 오류 수정 완료 | 미충족 |
| 10 | 주요 오류 없이 2주 이상 파일럿 운영 | 미충족 |

---

## 11. MVP 구현 체크리스트

> 설계 문서 `HRM_Automation_System_Design_v0.4.md` § 14.2에서 이관.
> 각 카테고리는 대응하는 Phase와 연결된다. 항목 완료 시 `- [x]`로 표시한다.

---

### 인프라 `→ Phase 1`

- [ ] Ubuntu 서버 준비 (Ubuntu 24.04 LTS 이상)
- [ ] Docker Engine 설치
- [ ] Docker Compose Plugin 설치
- [ ] `/App/hrmngr/` 기준 경로 디렉토리 구조 생성
  ```bash
  mkdir -p /App/hrmngr/{backend,frontend,data/postgres,data/redis,backup/postgres,logs}
  ```
- [ ] `docker-compose.yml` 작성 (api / web / db / redis / worker 5개 서비스)
- [ ] `.env` 파일 작성 및 `.gitignore` 설정 (`.env`, `data/`, `backup/postgres/*.sql.gz`, `logs/` 제외)
- [ ] Git Repository 초기화
- [ ] 방화벽(UFW) 설정 — 포트 3030, 8000 허용 / 포트 5442 내부망 제한

---

### 데이터베이스 `→ Phase 2`

- [ ] PostgreSQL Docker 컨테이너 구성 (외부 포트 **5442** → 내부 5432)
- [ ] `/App/hrmngr/data/postgres/` 바인드 마운트 확인
- [ ] Alembic 마이그레이션 환경 구성 (`env.py` 설정)
- [ ] 전체 테이블 생성 (15개)
  - [ ] `HR_DEPT_MST` — 부서 마스터
  - [ ] `HR_JIKGUP_MST` — 직급 마스터
  - [ ] `HR_JIKMU_MST` — 직무 마스터
  - [ ] `HR_SKILL_MST` — 기술 마스터
  - [ ] `HR_EMPL_MST` — 사원 마스터
  - [ ] `HR_EMPL_SKILL_REL` — 사원기술 연결
  - [ ] `HR_AVAIL_SNAP` — 가동가능 스냅샷
  - [ ] `PJT_MST` — 프로젝트 마스터
  - [ ] `PJT_ASGN_HIS` — 투입 이력
  - [ ] `PJT_RSRC_REQ` — 리소스 요청
  - [ ] `PJT_RCMD_RSLT` — 추천 결과
  - [ ] `SYS_USER_MST` — 시스템 사용자 마스터
  - [ ] `SYS_ROLE_MST` — 역할 마스터
  - [ ] `SYS_AUDIT_LOG` — 감사 로그
  - [ ] `SYS_BATCH_HIS` — 배치 실행 이력
- [ ] Seed 데이터 입력: `SYS_ROLE_MST` (6종) + `HR_JIKGUP_MST` + `HR_JIKMU_MST` (12종)
- [ ] DB 백업 스크립트 작성 (`/App/hrmngr/backup/backup_db.sh`) 및 crontab 등록 (매일 02:00)
- [ ] 복구 테스트 완료 (백업 파일 → 신규 DB 복구 확인)
- [ ] 외부 DB 클라이언트 접속 확인 (DBeaver 등, `localhost:5442`)

---

### 백엔드 `→ Phase 3`

- [ ] FastAPI 프로젝트 구조 생성 (`app/core/`, `app/models/`, `app/schemas/`, `app/api/v1/`, `app/services/`)
- [ ] SQLAlchemy 2.x ORM 모델 작성 (15개 테이블 전체)
- [ ] Pydantic v2 스키마 작성
- [ ] `/health` 헬스체크 엔드포인트 구현
- [ ] JWT 인증 API 구현 (`SYS_USER_MST` 기반 — 로그인, 토큰 갱신, 로그아웃)
- [ ] CORS 설정 적용 (포트 3030 허용)
- [ ] RBAC 권한 미들웨어 구현 (`SYS_ROLE_MST` 6개 역할)
- [ ] `SYS_AUDIT_LOG` 감사 로그 미들웨어 구현
- [ ] 사원 CRUD API (`HR_EMPL_MST` — `JIKMU_ID` 필드 포함)
- [ ] 직무 유형 CRUD API (`HR_JIKMU_MST`)
- [ ] 기술 CRUD API (`HR_SKILL_MST`, `HR_EMPL_SKILL_REL`)
- [ ] 부서/직급 코드 API (`HR_DEPT_MST`, `HR_JIKGUP_MST`)
- [ ] 프로젝트 CRUD API (`PJT_MST`)
- [ ] 투입 관리 API (`PJT_ASGN_HIS`)
- [ ] 가동률 계산 API (`HR_AVAIL_SNAP`)
- [ ] 리소스 검색/추천 API (`PJT_RSRC_REQ`, `PJT_RCMD_RSLT`)
- [ ] 대시보드 집계 API (직무 유형별 분포 포함)
- [ ] Excel Import/Export API
- [ ] 페이지네이션 공통 처리 구현
- [ ] OpenAPI 문서 확인 (`http://{서버IP}:8000/docs`)

---

### 프론트엔드 `→ Phase 4`

- [ ] Next.js 프로젝트 생성 (`output: 'standalone'` 설정 필수)
- [ ] `NEXT_PUBLIC_API_BASE_URL` 환경변수 설정 (`http://{서버IP}:8000`)
- [ ] 로그인 화면 구현 (`/login`)
- [ ] 공통 레이아웃·네비게이션 구현 (권한별 메뉴 제어)
- [ ] 대시보드 구현 (`/dashboard` — 직무 유형 분포 위젯 포함)
- [ ] 사원 관리 화면 구현 (`/employees` — `JIKMU_ID` 필드·직무 유형 필터 포함)
- [ ] 사원 상세 화면 구현 (`/employees/[id]`)
- [ ] 기술 관리 화면 구현 (`/skills`, `HR_SKILL_MST`)
- [ ] 직무 유형 관리 화면 구현 (`/job-types`, `HR_JIKMU_MST`)
- [ ] 프로젝트 목록/상세 화면 구현 (`/projects`, `/projects/[id]`)
- [ ] 투입 관리 화면 구현 (`/assignments`, `PJT_ASGN_HIS`)
- [ ] 가동 가능 인력 조회 화면 구현 (`/availability` — 직무 유형 필터 포함)
- [ ] 리소스 추천 화면 구현 (`/recommendations`, `PJT_RCMD_RSLT`)
- [ ] AI Chat 화면 구현 (`/ai-chat`)
- [ ] 리포트 화면 구현 (`/reports`)
- [ ] 설정 화면 구현 (`/settings/users`, `/settings/audit-logs`)
- [ ] Excel Import/Export UI 구현

---

### 리소스 검색 및 추천 `→ Phase 5`

- [ ] 가동 가능일 자동 계산 로직 구현 (`HR_AVAIL_SNAP` 기반)
- [ ] 즉시 투입 가능 인력 조회 API 구현 (`AVAIL_STAT_CD='AVAILABLE'`)
- [ ] 직무 유형·기술·숙련도 복합 필터 검색 API 구현
- [ ] 추천 점수 산정 로직 구현
  - 직무 유형 일치 15% + 기술 매칭 35% + 숙련도 25% + 가동일 15% + 유사 경험 7% + 역할 적합도 3%
- [ ] `PJT_RSRC_REQ` 인력 요청 등록 API 구현
- [ ] `PJT_RCMD_RSLT` 추천 결과 저장 및 조회 API 구현

---

### AI 질의응답 `→ Phase 6`

- [ ] LLM 호출 레이어 추상화 (OpenAI/Anthropic/사내 LLM 전환 가능 구조)
- [ ] 자연어 조건 파싱 구현 (`JIKMU_CD`, `SKILL_NM`, 가동일 키워드 인식 포함)
- [ ] 파싱 결과 → SQL 조회 → 결과 요약 흐름 구현
- [ ] 권한 필터링 후 LLM 컨텍스트 전달 구현
- [ ] 환각 방지 시스템 프롬프트 적용
- [ ] `POST /api/v1/ai/chat` 엔드포인트 구현
- [ ] 테스트 질의 10개 이상 검증 (직무 유형 포함 질의 반드시 포함)

---

### 운영 자동화 및 배포 `→ Phase 7`

- [ ] `HR_AVAIL_SNAP_GEN` 배치 구현 (매일 01:00 — 가동가능 스냅샷 생성)
- [ ] `PJT_ASGN_END_ALERT` 배치 구현 (매주 금요일 17:00 — 30일 이내 종료 예정 알림)
- [ ] `HR_DATA_QUALITY_CHK` 배치 구현 (매주 금요일 18:00 — `JIKMU_ID IS NULL` 점검 포함)
- [ ] `PJT_WEEKLY_RPT` 배치 구현 (매주 월요일 09:00 — 주간 리포트 발송)
- [ ] `SYS_DB_BACKUP` 배치 구현 및 crontab 등록 (매일 02:00)
- [ ] Teams Webhook 알림 연동
- [ ] 구조화 로그(JSON 포맷) 설정
- [ ] Docker 컨테이너 재기동 절차 문서화
- [ ] `restart: unless-stopped` 자동 재기동 설정 확인
- [ ] Nginx 도입 여부 검토 (HTTPS/도메인 필요 시)

---

### 파일럿 운영 및 데이터 이관 `→ Phase 8`

- [ ] 기존 Excel 데이터 `HR_EMPL_MST` 등으로 일괄 이관
- [ ] `HR_EMPL_MST.JIKMU_ID` 직무 유형 수동 보정
- [ ] 파일럿 사용자 계정 생성 (`SYS_USER_MST` — PM·운영팀장·팀장 역할)
- [ ] 파일럿 사용자 테스트 수행 및 오류 수집
- [ ] 정식 운영 전환 기준 10개 항목 최종 점검 (§ 10 참조)
- [ ] 전사 공지 및 사용자 교육 자료 배포
- [ ] 정식 운영 선언

---

## 12. 변경 이력

| 날짜 | 버전 | 변경 내용 | 작성자 |
|---|---|---|---|
| 2026-07-01 | v0.1 | ROADMAP 최초 작성 (Phase 0~8 구성, 기능·기술 요소 상태표, 리스크 초안) | — |
| 2026-07-01 | v0.2 | 설계 문서(v0.4) § 14.2 MVP 완료 체크리스트를 §11로 이관 — 인프라/DB/백엔드/프론트엔드/검색추천/AI/운영자동화/파일럿 8개 카테고리, 각 Phase 연결, 테이블 수준 세부 항목 추가 | — |

