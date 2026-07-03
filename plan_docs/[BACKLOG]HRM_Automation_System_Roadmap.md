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
| Phase 1 | 인프라 및 개발환경 구축 | 2주차 | 진행 중 | 60% | 정상 |
| Phase 2 | PostgreSQL 데이터 모델 구축 | 2~3주차 | 진행 중 | 60% | 정상 |
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
| **개발 상태** | 진행 중 |
| **진행률** | 60% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| Ubuntu Server 24.04 LTS 환경 준비 | 완료 |
| Docker Engine 설치 | 완료 |
| Docker Compose Plugin 설치 | 예정 (현재 `docker-compose` v1.29.2만 설치됨 — v2 플러그인 전환 필요) |
| `/App/hrmngr/` 디렉토리 구조 생성 | 완료 (`backend/`, `frontend/`, `data/postgres/`, `data/redis/`, `backup/postgres/`, `logs/`) |
| `docker-compose.yml` 초안 작성 (api / web / db / redis / worker) | 완료 (`docker-compose config`로 문법 검증 완료) |
| 전 컨테이너 타임존 KST(Asia/Seoul) 통일 | 완료 (2026-07-03 — `TZ`/`PGTZ` 환경변수 + `/etc/localtime`·`/etc/timezone` 읽기전용 바인드 마운트, YAML anchor로 중복 최소화. 실 컨테이너 기동 후 `date`/`SHOW timezone;` 검증은 서버에서 수행 필요) |
| `.env` 파일 작성 및 `.gitignore` 설정 | 완료 (`.env.example` 작성, `.gitignore`에 `data/`, `backup/postgres/*.sql.gz`, `logs/`, `.next/` 추가) |
| Git Repository 초기화 | 완료 (기존 리포지토리) |
| PostgreSQL 컨테이너 기동 및 포트 5442 접속 확인 | 예정 (개발 환경 권한 제약으로 미검증 — 서버에서 확인 필요) |
| FastAPI 컨테이너 기동 및 `/health` 응답 확인 | 예정 (최소 `/health` 엔드포인트 스켈레톤은 작성 완료, 컨테이너 기동 미검증) |
| Next.js 컨테이너 기동 및 포트 3030 접속 확인 | 예정 (Dockerfile 작성 완료, 기동 미검증) |
| 방화벽(UFW) 설정 (3030, 8000 허용 / 5442 내부망 제한) | 예정 |

**산출물**

- `docker-compose.yml` — 완료
- `.env.example` — 완료
- `.gitignore` — 완료
- `README.md` (기동 명령어 포함) — 완료
- `backend/Dockerfile`, `backend/requirements.txt`, `backend/app/main.py`(`/health`), `backend/app/core/config.py` — 완료 (Phase 3에서 본격 확장 예정)
- `frontend/Dockerfile`, `frontend/next.config.mjs`(`output: 'standalone'`) — 완료
- `backup/backup_db.sh` — 완료 (crontab 등록은 서버에서 별도 수행 필요)

**완료 기준**

- `docker compose up -d` 한 번으로 api / web / db / redis / worker 5개 컨테이너 모두 정상 기동 — 미검증 (샌드박스 환경 Docker 소켓 권한 제약, 실서버에서 확인 필요)
- `http://{서버IP}:3030` Next.js 초기 화면 접근 가능 — 미검증
- `http://{서버IP}:8000/health` FastAPI 헬스체크 응답 확인 — 미검증
- `localhost:5442` PostgreSQL 외부 접속 확인 (DBeaver 등) — 미검증

**참고**

- 2026-07-02 기준 개발 환경에서 `docker-compose config`로 compose 파일 문법 검증까지는 완료. 실제 컨테이너 기동/헬스체크/포트 접속 확인은 Docker 소켓 접근 권한이 있는 실 서버 환경에서 이어서 수행 필요.

---

### Phase 2. PostgreSQL 데이터 모델 구축

| 항목 | 내용 |
|---|---|
| **목표** | 한국 HR META 명명 규칙 기반 전체 테이블 생성 및 초기 데이터 적재 |
| **계획 기간** | 2~3주차 |
| **개발 상태** | 진행 중 |
| **진행률** | 60% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| ERD 최종 확정 | 완료 (`backend/docs/ERD.md`, 2026-07-02) |
| Alembic 마이그레이션 환경 구성 | 완료 (`backend/alembic.ini`, `backend/alembic/env.py`, 2026-07-03 — 실 DB 연결 검증은 미실행, 아래 §3 참조) |
| `HR_DEPT_MST` (부서 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `HR_JIKGUP_MST` (직급 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `HR_JIKMU_MST` (직무 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `HR_SKILL_MST` (기술 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `HR_EMPL_MST` (사원 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `HR_EMPL_SKILL_REL` (사원기술 연결) 테이블 생성 | 예정 |
| `HR_EMPL_ROLE_REL` (사원역할 연결, 복수 직무 지원) 테이블 생성 | 예정 |
| `PJT_MST` (프로젝트 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `PJT_ASGN_HIS` (투입 이력) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `PJT_RSRC_REQ` (리소스 요청) 테이블 생성 | 예정 |
| `PJT_RCMD_RSLT` (추천 결과) 테이블 생성 | 예정 |
| `HR_AVAIL_SNAP` (가동가능 스냅샷) 테이블 생성 | 예정 |
| `SYS_USER_MST` (사용자 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `SYS_ROLE_MST` (역할 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `SYS_AUDIT_LOG` (감사 로그) 테이블 생성 | 완료 (모델+마이그레이션 작성, 2026-07-03 — 실 DB 적용 미검증) |
| `SYS_BATCH_HIS` (배치 이력) 테이블 생성 | 예정 |
| Seed 데이터 입력 (`SYS_ROLE_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST` 12종) | 진행 중 — `SYS_ROLE_MST` 6종은 마이그레이션에 포함 완료(`83fc676b952e_create_sys_user_role_audit_tables.py`), `HR_JIKGUP_MST`(10종)/`HR_JIKMU_MST`(12종)는 아직 Seed 스크립트 미작성 |
| DB 백업 스크립트 작성 및 crontab 등록 (매일 02:00) | 예정 |

**산출물**

- Alembic 마이그레이션 스크립트 (전체 테이블)
- Seed 데이터 SQL 또는 Python 스크립트
- `backup_db.sh`

**완료 기준**

- `alembic upgrade head` 실행 후 16개 테이블 전부 생성 확인
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
| SQLAlchemy 2.x ORM 모델 작성 (16개 테이블) | 예정 |
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
| 가동 가능일 자동 계산 로직 구현 (`HR_AVAIL_SNAP` 기반, MVP 산정 기준 확정 — `backend/docs/AVAILABILITY_CALC_SPEC.md` 참조) | 예정 |
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
| 가동 가능일 자동 계산 | `HR_AVAIL_SNAP` 기반 산정 | 예정 | 높음 | `availability_service.py`, `HR_AVAIL_SNAP_GEN` 배치 | 투입률 0%=AVAILABLE(기준일), 1~99%=PARTIAL(기준일), ≥100%=FULL(MAX(종료일)+1, 종료일 NULL 시 품질경고) — `PROPOSED` 제외, 상세는 `backend/docs/AVAILABILITY_CALC_SPEC.md` |
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

### 2026-07-02

- Phase 1 인프라 구축 착수
- `/App/hrmngr/` 하위 디렉토리 구조 생성 (`backend/`, `data/postgres/`, `data/redis/`, `backup/postgres/`, `logs/`)
- `docker-compose.yml` 작성 완료 (api / web / db / redis / worker 5개 서비스, 설계 문서 §8.3 스펙 반영, `docker-compose config` 문법 검증 완료)
- `.env.example` 작성 완료 (설계 문서 §8.7 변수 전체 반영)
- `.gitignore`에 `data/`, `backup/postgres/*.sql.gz`, `logs/`, `.next/` 추가
- `README.md` 작성 (기동/재기동/백업 명령어 포함)
- `backend/` FastAPI 프로젝트 기본 구조 생성 (`app/core/`, `app/db/`, `app/models/`, `app/schemas/`, `app/repositories/`, `app/services/`, `app/api/v1/`, `alembic/`, `tests/`) 및 `/health` 엔드포인트 최소 스켈레톤 구현
- `backend/Dockerfile`, `backend/requirements.txt` 작성
- `frontend/Dockerfile` (pnpm 기반 3-stage 빌드) 및 `next.config.mjs`에 `output: 'standalone'` 추가
- `backup/backup_db.sh` 작성 및 실행 권한 부여
- 컨테이너 실기동·헬스체크·UFW 방화벽 설정은 Docker 소켓 접근 권한 제약으로 미검증 — 실 서버에서 후속 확인 필요
- (§8 다음 작업 1번) PostgreSQL ERD 최종 확정 — 설계 문서(수정 없이 원본 유지) §5 기준 15개 테이블 전체 컬럼·PK/FK·CHECK 제약·Seed 데이터·카디널리티를 `backend/docs/ERD.md`로 정리 완료. Alembic 마이그레이션(§8 4번) 작성의 근거 자료로 확정
- ERD 정리 과정에서 발견한 미확정 사항 3건을 §9 리스크에 추가 (`HR_EMPL_ROLE_REL` 범위 포함 여부, `SYS_ROLE_MST` 세부 값 미정, `PJT_RCMD_RSLT` 추천 가중치 표기 불일치)
- (관계자 확인 완료) `HR_EMPL_ROLE_REL`(사원역할 연결, 복수 직무 지원) 테이블을 Phase 2 데이터 모델 범위에 포함하기로 확정 — 로드맵 전체의 "15개 테이블" 표현을 "16개 테이블"로 정정, §4 Phase 2 테이블 생성 목록·§11 MVP 체크리스트(데이터베이스/백엔드)에 `HR_EMPL_ROLE_REL` 추가, §9 리스크 중 해당 항목 해결 처리
- `HR_SKILL_MST` 초기 Seed MVP 초안 작성 (`backend/app/db/seed/hr_skill_mst_seed.py`, 55건) — BACKEND/FRONTEND/ARCHITECTURE/CLOUD/BUSINESS/DESIGN 6개 그룹, 한국 SI/IT 조직 통상 기술 스택 기준. `backend/docs/ERD.md` §3.4에 초안 표기 및 근거 추가. §9 리스크 "직원 기술 스택 표준화 기준 미정" 상태를 "차단→주의"로 하향 (운영팀 최종 확정 전까지 MVP 표기 유지)
- `SYS_ROLE_MST` 초기 Seed MVP 확정 (`backend/app/db/seed/sys_role_mst_seed.py`) — ROLE_CD 6종(ADMIN/HR_MGR/PM/TEAM_LEAD/EXEC/VIEWER) 유지, ROLE_NM/ROLE_DESC 및 화면 단위 `PERM_JSON`(`{"screens": {...: "edit"|"view"|"none"}}`) 작성. `backend/docs/ERD.md` §3.13 갱신. §9 리스크 "인증/권한 범위 미정", "`SYS_ROLE_MST` 세부 값 미정" 2건을 "해결(MVP)"로 처리
- MVP 권한 매트릭스(화면 접근 + 버튼 권한) 작성 — `backend/docs/PERMISSION_MATRIX.md` 신규. 화면 접근 권한은 `[DESIGN]HRM_Screen_Design.md` "화면 목록" 표의 역할 기준(SCR-001~016)을 그대로 따르고, 버튼 권한은 조회/등록/수정/삭제/Excel/관리자 기능 6개 카테고리로 세분화. `sys_role_mst_seed.py`의 `PERM_JSON`을 단순 화면 단위(`edit`/`view`/`none`) 구조에서 화면×버튼 세부 구조(각 6개 boolean)로 v2 갱신, `backend/docs/ERD.md` §3.13 근거 링크 갱신. 화면 설계서에 역할 제한이 명시되지 않은 일부 버튼(예: 프로젝트 등록, 리포트 Excel/발송)은 인접 권한 그룹 기준으로 추정 처리하고 `PERMISSION_MATRIX.md` §5에 운영팀 확인 필요 사항으로 별도 기록

---

### 2026-07-03

- 가동 가능일 MVP 산정 기준 확정 — `backend/docs/AVAILABILITY_CALC_SPEC.md` 신규 작성. 기준일=`HR_AVAIL_SNAP.SNAP_DT`(배치 실행일), 투입률 합계 산정 대상 조건(`ASGN_STAT_CD='ACTIVE'`, `ASGN_STRT_DT<=기준일`, `ASGN_END_DT IS NULL OR ASGN_END_DT>=기준일`, `ASGN_TYPE_CD IN ('RUNNING','COMMITTED')`), `PROPOSED` 기본 제외(대시보드/리포트 "전체(+제안중)" 지표로 별도 표시), 0%/1~99%/≥100% 3단계 `AVAIL_STAT_CD`·`AVAIL_STRT_DT` 산정식(종료일 NULL 시 데이터 품질 경고 처리 포함), 100% 초과 데이터의 저장 차단 원칙 및 기존 Excel 이관 데이터 예외(품질 점검 경고 대상) 확정. §9 리스크 "가동 가능일 계산 기준 미정" 상태를 "차단→주의"로 하향, §11 MVP 체크리스트 관련 항목 설명 갱신
- (§8 다음 작업 4번) PostgreSQL 초기 마이그레이션 구성(Alembic `env.py` 설정) 완료 — `backend/alembic.ini`(민감정보 미포함, `DATABASE_URL`은 `.env` 기반으로 `env.py`에서 로드), `backend/alembic/env.py`(offline/online 마이그레이션 모드 지원, `app.db.base.Base.metadata`를 target_metadata로 사용), `backend/alembic/script.py.mako`(리비전 템플릿), `backend/alembic/versions/`(빈 디렉토리) 신규 작성. `backend/app/db/base.py`에 공통 `Base` 선언 추가, `app/models/__init__.py`에 Phase 2 모델 등록 안내 주석 추가. README.md에 Alembic 사용법(리비전 생성/적용/롤백) 섹션 추가. **실 DB 연결 기반 `alembic upgrade head` 실행은 로컬 환경에 `alembic`/`pip` 미설치로 미검증** — 구문·설정 파일 유효성만 확인 (아래 검증 결과 참조)
- 전 컨테이너 타임존 KST(Asia/Seoul) 통일 — `docker-compose.yml`의 `api`/`web`/`worker`/`db`/`redis` 5개 서비스에 `TZ=Asia/Seoul` 적용(YAML anchor `x-tz-env`로 중복 최소화), Ubuntu 호스트 `/etc/localtime`·`/etc/timezone` 읽기전용 바인드 마운트 추가, PostgreSQL은 `PGTZ=Asia/Seoul` 추가 지정(단 `TIMESTAMPTZ` 내부 저장은 UTC 유지). `.env`에는 `TZ` 추가하지 않음(compose 레벨 anchor로 고정). 설계서(`[DESIGN]HRM_Automation_System_Design_v0_6.md`) §8.3을 동일 내용으로 갱신하고 §8.3-1(타임존 정책, Alpine tzdata 참고사항, 운영 검증 명령)을 신규 추가 — 업무/DB/화면/API 설계 내용은 변경 없음. Dockerfile은 이번 작업에서 수정하지 않음(Alpine tzdata 이슈 미확인, 필요 시 후속 검토 사항으로 문서화)
- §9 리스크 및 차단 이슈 표 구조 변경 — `처리일자` 컬럼 신규 추가, `상태` 열 값을 상태값 단일 표기(차단/주의/해소)로 정리하고 날짜는 `처리일자`로 분리. 이슈·대응 방안 실질 내용은 변경 없음
- (§8 다음 작업 5번) `HR_DEPT_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST`, `HR_SKILL_MST`, `HR_EMPL_MST`, `PJT_MST`, `PJT_ASGN_HIS` 7개 테이블 생성 — `backend/app/db/base.py` 기준 SQLAlchemy 2.x ORM 모델 7종을 `backend/app/models/`에 신규 작성(`hr_dept_mst.py`, `hr_jikgup_mst.py`, `hr_jikmu_mst.py`, `hr_skill_mst.py`, `hr_empl_mst.py`, `pjt_mst.py`, `pjt_asgn_his.py`), 공통 `REG_DTTM`/`UPD_DTTM`(+`REG_USER`/`UPD_USER`) 컬럼을 위한 `TimestampMixin`/`AuditMixin`을 `app/models/mixins.py`에 추가. 스키마는 `backend/docs/ERD.md` §3.1~3.5, 3.8~3.9 그대로 반영(컬럼 타입·PK/FK·CHECK 제약 포함). `app/models/__init__.py`에 7개 모델 import 등록. Alembic 리비전 `backend/alembic/versions/28ce52377e32_create_core_hr_pjt_tables.py`를 수기 작성(로컬 환경에 `alembic` 패키지 미설치로 `--autogenerate` 실행 불가하여 모델 정의 기준으로 직접 작성). `PJT_ASGN_HIS.ALLOC_RT` 100% 초과 방지 등 테이블 간 데이터 정합성 규칙은 DB 제약만으로 표현 불가하여 서비스 레이어 구현(Phase 3) 몫으로 모델 주석에 명시. **부분 완료**: ERD 16개 테이블 중 7개만 처리, 나머지 9개(`HR_EMPL_SKILL_REL`, `HR_EMPL_ROLE_REL`, `HR_AVAIL_SNAP`, `PJT_RSRC_REQ`, `PJT_RCMD_RSLT`, `SYS_USER_MST`, `SYS_ROLE_MST`, `SYS_AUDIT_LOG`, `SYS_BATCH_HIS`)는 §8 6번 이후 작업. **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경에 `alembic`/`psycopg`/`pip` 미설치로 미실시** — Python 구문 검증만 완료 (아래 검증 결과 참조)
- (§8 다음 작업 6번) `SYS_USER_MST`, `SYS_ROLE_MST`, `SYS_AUDIT_LOG` 3개 테이블 생성 및 Seed 데이터 입력 — SQLAlchemy 모델 3종(`sys_role_mst.py`, `sys_user_mst.py`, `sys_audit_log.py`)을 `backend/docs/ERD.md` §3.12~3.14 기준으로 신규 작성. `SYS_ROLE_MST`는 REG_DTTM/UPD_DTTM 컬럼이 없어(설계서 원본 그대로) Mixin 미적용, `SYS_AUDIT_LOG`는 REG_DTTM만 있어(append-only 로그 성격) 별도 Mixin 없이 직접 선언. `ENCR_PWD` 해싱·`BFR_VAL_JSON`/`AFT_VAL_JSON` 마스킹 등 보안 처리는 Phase 3 구현 몫으로 모델 주석에 명시. Alembic 리비전 `backend/alembic/versions/83fc676b952e_create_sys_user_role_audit_tables.py`를 이전 리비전(`28ce52377e32`) 뒤에 체이닝해 수기 작성, 기존 `app/db/seed/sys_role_mst_seed.py`를 재사용해 `SYS_ROLE_MST` 6종 Seed를 `op.bulk_insert`로 함께 반영. **부분 완료**: `HR_JIKGUP_MST`/`HR_JIKMU_MST` Seed(10/12종)는 아직 스크립트 미작성 — §11 Seed 체크리스트 항목은 미완료 유지. **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)

---

## 8. 다음 작업

> 개발자가 Phase 1~2 시작 시 즉시 수행할 수 있는 작업 단위.
> 순서대로 수행하는 것을 권장한다.

- [ ] 0. (Phase 1 마무리) 실 서버에서 `docker compose up -d --build` 기동 확인, UFW 방화벽 설정, Docker Compose Plugin v2 전환
- [x] 1. PostgreSQL ERD 최종 확정 (`HR_EMPL_MST` 등 16개 테이블 관계 검토, `HR_EMPL_ROLE_REL` 포함 확정) → `backend/docs/ERD.md`
- [x] 2. Docker Compose 개발환경 구성 (`docker-compose.yml` 작성 — api / web / db / redis / worker)
- [x] 3. FastAPI 프로젝트 기본 구조 생성 (`app/`, `models/`, `schemas/`, `api/v1/`, `core/`)
- [x] 4. PostgreSQL 초기 마이그레이션 구성 (Alembic `env.py` 설정) → `backend/alembic.ini`, `backend/alembic/env.py` (실 DB 연결 `alembic upgrade` 검증은 미실행 — 아래 검증 결과 참조)
- [x] 5. `HR_DEPT_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST`, `HR_SKILL_MST`, `HR_EMPL_MST`, `PJT_MST`, `PJT_ASGN_HIS` 테이블 생성 → SQLAlchemy 모델(`backend/app/models/`) + Alembic 마이그레이션(`backend/alembic/versions/28ce52377e32_create_core_hr_pjt_tables.py`) 작성 완료. 실 DB 연결 기반 `alembic upgrade head` 적용 검증은 미실행 (아래 검증 결과 참조)
- [x] 6. `SYS_USER_MST`, `SYS_ROLE_MST`, `SYS_AUDIT_LOG` 테이블 생성 및 Seed 데이터 입력 → SQLAlchemy 모델(`backend/app/models/`) + Alembic 마이그레이션(`backend/alembic/versions/83fc676b952e_create_sys_user_role_audit_tables.py`, `SYS_ROLE_MST` 6종 Seed 포함) 작성 완료. 실 DB 적용 검증은 미실행 (아래 §3 검증 결과 참조)
- [ ] 7. 사원 목록 조회 API 구현 (`GET /api/v1/employees`)
- [ ] 8. 사원 등록/수정 API 구현 (`POST`, `PATCH /api/v1/employees`)
- [ ] 9. Next.js 기본 레이아웃 구성 (로그인 화면, 공통 네비게이션)
- [ ] 10. 사원 목록 화면 구현 (`/employees` — 직무 유형 필터 포함)
- [ ] 11. 프로젝트 투입 현황 화면 구현 (`/assignments`)

---

## 9. 리스크 및 차단 이슈

| 이슈 | 영향도 | 상태 | 대응 방안 | 처리일자 |
|---|---|---|---|---|
| 직원 기술 스택 표준화 기준 미정 | 높음 | 주의 | `HR_SKILL_MST` MVP 초안 55건(BACKEND/FRONTEND/ARCHITECTURE/CLOUD/BUSINESS/DESIGN 6개 그룹) 작성 완료 — `backend/app/db/seed/hr_skill_mst_seed.py`, `backend/docs/ERD.md` §3.4 참조. 초안이 마련되어 Phase 2 Alembic Seed 작업 착수는 가능하나, 운영팀 최종 확정 전까지는 MVP 표기 유지 및 실 데이터 반영 보류 — 확정 후 "해소"로 재변경 | 2026-07-02 |
| 가동 가능일 계산 기준 미정 | 높음 | 주의 | MVP 산정 기준 확정 완료 — 기준일은 `HR_AVAIL_SNAP.SNAP_DT`(배치 실행일), 투입률 합계는 `ASGN_STAT_CD='ACTIVE' AND ASGN_STRT_DT<=기준일 AND (ASGN_END_DT IS NULL OR ASGN_END_DT>=기준일) AND ASGN_TYPE_CD IN ('RUNNING','COMMITTED')` 조건의 `PJT_ASGN_HIS`만 집계(`PROPOSED`는 기본 산정에서 제외, 대시보드/리포트 "전체(+제안중)" 지표로만 별도 표시). 0%=`AVAILABLE`(기준일), 1~99%=`PARTIAL`(기준일), ≥100%=`FULL`(`MAX(ASGN_END_DT)+1일`, 단 종료일 NULL 존재 시 `AVAIL_STRT_DT=NULL`+데이터 품질 경고). 100% 초과는 원칙적으로 저장 차단하되 기존 Excel 이관 데이터는 품질 점검 경고 대상으로 예외 처리. 상세는 `backend/docs/AVAILABILITY_CALC_SPEC.md` 참조. 운영팀 최종 확정 전까지 MVP 표기 유지 | 2026-07-03 |
| 인증/권한 범위 미정 | 높음 | 해소 | `SYS_ROLE_MST` 6개 역할 및 화면×버튼(조회/등록/수정/삭제/Excel/관리자 기능) 권한 매트릭스 MVP 확정 완료 — `backend/docs/PERMISSION_MATRIX.md`(매트릭스 근거), `backend/app/db/seed/sys_role_mst_seed.py`(Seed), `backend/docs/ERD.md` §3.13 참조. 화면 설계서에 명시 없는 일부 버튼 권한은 추정치이며 `PERMISSION_MATRIX.md` §5에 운영팀 확인 필요 사항으로 별도 정리 | 2026-07-02 |
| AI 질의응답 연동 범위 미정 | 중간 | 주의 | MVP는 OpenAI/Anthropic API 연동, 보안 요건에 따라 사내 LLM 전환 — Phase 5 완료 후 결정 | - |
| 기존 Excel/SharePoint 데이터 마이그레이션 방식 미정 | 높음 | 주의 | Excel Import 기능 구현 (Phase 3) 후 데이터 정제 절차 수립 — Phase 8 전 완료 목표 | - |
| 운영 서버 백업 정책 미정 | 중간 | 주의 | `pg_dump` 매일 02:00 + 14일 보관 + 외부 스토리지 복제 초안 제시, 운영팀 확인 필요 | - |
| 서버 HTTPS/도메인 미적용 | 낮음 | 주의 | 초기 구축은 내부망 HTTP로 운영, Phase 7에서 Nginx + TLS 도입 여부 재검토 | - |
| `HR_EMPL_MST.JIKMU_ID` 기존 데이터 없음 | 낮음 | 주의 | NULL 허용 설계로 이관 후 운영팀 수동 보정, Phase 8 데이터 이관 시 처리 | - |
| 컨테이너 타임존이 Ubuntu 호스트 설정에 종속 | 낮음 | 주의 | `/etc/localtime`·`/etc/timezone` 바인드 마운트 방식이라 호스트 자체가 KST(Asia/Seoul)로 설정되어 있어야 컨테이너도 KST가 됨 — 배포 전 `timedatectl set-timezone Asia/Seoul` 확인 필요. Alpine 이미지(`redis`, `db`, `web`)는 `tzdata` 미설치 시 일부 CLI가 `TZ` 이름을 못 찾을 수 있음(바인드 마운트로 우회되나 완전 검증은 실 서버에서 필요) — 상세는 설계서 §8.3-1, `docker-compose.yml` 참조 | 2026-07-03 |
| `HR_EMPL_ROLE_REL` 테이블 범위 포함 여부 미정 | 중간 | 해소 | 관계자 확인 완료 — Phase 2 데이터 모델 범위에 포함 확정. 로드맵 전체 테이블 수를 "15개→16개"로 정정, §4/§11 테이블 목록에 반영 완료 (`backend/docs/ERD.md` §5 참조) | 2026-07-02 |
| `SYS_ROLE_MST` 세부 값(ROLE_NM/ROLE_DESC/PERM_JSON) 미정 | 중간 | 해소 | ROLE_NM/ROLE_DESC 및 화면×버튼 권한(`view`/`create`/`update`/`delete`/`excel`/`admin`) 기준 PERM_JSON MVP 확정 완료 — `backend/app/db/seed/sys_role_mst_seed.py`, `backend/docs/PERMISSION_MATRIX.md` 참조 | 2026-07-02 |
| `PJT_RCMD_RSLT` 추천 점수 가중치 표기 불일치 | 낮음 | 주의 | 설계 문서 §5 인용 구간과 로드맵 §4 Phase 5·§11 명시 가중치 수치가 다르게 표기됨 — Phase 5 착수 시 로드맵 수치(직무 15%+기술 35%+숙련도 25%+가동일 15%+유사경험 7%+역할적합도 3%)로 확정 예정 | - |

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

- [x] Ubuntu 서버 준비 (Ubuntu 24.04 LTS 이상)
- [x] Docker Engine 설치
- [ ] Docker Compose Plugin 설치 (현재 `docker-compose` v1.29.2만 설치됨, v2 플러그인 전환 필요)
- [x] `/App/hrmngr/` 기준 경로 디렉토리 구조 생성
  ```bash
  mkdir -p /App/hrmngr/{backend,frontend,data/postgres,data/redis,backup/postgres,logs}
  ```
- [x] `docker-compose.yml` 작성 (api / web / db / redis / worker 5개 서비스)
- [x] `.env` 파일 작성 및 `.gitignore` 설정 (`.env`, `data/`, `backup/postgres/*.sql.gz`, `logs/` 제외)
- [x] Git Repository 초기화
- [ ] 방화벽(UFW) 설정 — 포트 3030, 8000 허용 / 포트 5442 내부망 제한 (실 서버 sudo 권한 필요, 미실행)

---

### 데이터베이스 `→ Phase 2`

- [ ] PostgreSQL Docker 컨테이너 구성 (외부 포트 **5442** → 내부 5432)
- [ ] `/App/hrmngr/data/postgres/` 바인드 마운트 확인
- [x] Alembic 마이그레이션 환경 구성 (`env.py` 설정) — `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/script.py.mako`, `backend/app/db/base.py`(`Base` 선언) 작성 완료. 실 DB 연결 기반 `alembic upgrade head` 실행 검증은 미실시 (아래 §3 검증 결과 참조)
- [ ] 전체 테이블 생성 (16개, 10/16 모델+마이그레이션 작성 완료 — 실 DB 적용 미검증)
  - [x] `HR_DEPT_MST` — 부서 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [x] `HR_JIKGUP_MST` — 직급 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [x] `HR_JIKMU_MST` — 직무 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [x] `HR_SKILL_MST` — 기술 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [x] `HR_EMPL_MST` — 사원 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [ ] `HR_EMPL_SKILL_REL` — 사원기술 연결
  - [ ] `HR_EMPL_ROLE_REL` — 사원역할 연결 (복수 직무 지원)
  - [ ] `HR_AVAIL_SNAP` — 가동가능 스냅샷
  - [x] `PJT_MST` — 프로젝트 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [x] `PJT_ASGN_HIS` — 투입 이력 (모델+마이그레이션 작성, 2026-07-03)
  - [ ] `PJT_RSRC_REQ` — 리소스 요청
  - [ ] `PJT_RCMD_RSLT` — 추천 결과
  - [x] `SYS_USER_MST` — 시스템 사용자 마스터 (모델+마이그레이션 작성, 2026-07-03)
  - [x] `SYS_ROLE_MST` — 역할 마스터 (모델+마이그레이션 작성, 2026-07-03 — Seed 6종 포함)
  - [x] `SYS_AUDIT_LOG` — 감사 로그 (모델+마이그레이션 작성, 2026-07-03)
  - [ ] `SYS_BATCH_HIS` — 배치 실행 이력
- [ ] Seed 데이터 입력: `SYS_ROLE_MST` (6종, MVP 확정 — `backend/app/db/seed/sys_role_mst_seed.py`) + `HR_JIKGUP_MST` + `HR_JIKMU_MST` (12종) — `SYS_ROLE_MST`는 마이그레이션 `83fc676b952e_create_sys_user_role_audit_tables.py`에 `op.bulk_insert`로 반영 완료(실 DB 적용은 미검증). `HR_JIKGUP_MST`/`HR_JIKMU_MST` Seed 스크립트는 아직 미작성 (미완료 유지)
- [ ] `HR_SKILL_MST` Seed 입력 — MVP 초안 55건 작성 완료(`backend/app/db/seed/hr_skill_mst_seed.py`), 운영팀 최종 확정 후 실 데이터 반영 예정 (미완료 유지)
- [ ] DB 백업 스크립트 작성 (`/App/hrmngr/backup/backup_db.sh`) 및 crontab 등록 (매일 02:00)
- [ ] 복구 테스트 완료 (백업 파일 → 신규 DB 복구 확인)
- [ ] 외부 DB 클라이언트 접속 확인 (DBeaver 등, `localhost:5442`)

---

### 백엔드 `→ Phase 3`

- [ ] FastAPI 프로젝트 구조 생성 (`app/core/`, `app/models/`, `app/schemas/`, `app/api/v1/`, `app/services/`)
- [ ] SQLAlchemy 2.x ORM 모델 작성 (16개 테이블 전체)
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

- [ ] 가동 가능일 자동 계산 로직 구현 (`HR_AVAIL_SNAP` 기반, MVP 산정 기준 확정 — 기준일 `SNAP_DT` 기준 `ACTIVE`+`RUNNING/COMMITTED` 투입만 집계, `PROPOSED` 제외, 0%=`AVAILABLE`/1~99%=`PARTIAL`/≥100%=`FULL`(`MAX(ASGN_END_DT)+1`); 상세는 `backend/docs/AVAILABILITY_CALC_SPEC.md` 참조)
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
| 2026-07-02 | v0.3 | Phase 1 착수 — 디렉토리 구조, `docker-compose.yml`, `.env.example`, `.gitignore`, `README.md`, `backend`/`frontend` Dockerfile, FastAPI `/health` 스켈레톤, `backup_db.sh` 작성 완료. Phase 1 진행률 60%로 갱신. 컨테이너 실기동·UFW 설정은 실 서버 확인 대기 | — |
| 2026-07-02 | v0.4 | §8 다음 작업 1번(ERD 최종 확정) 완료 처리 — `backend/docs/ERD.md` 작성. Phase 2 진행률 5%로 갱신, 상태 "진행 중"으로 변경. ERD 정리 중 발견한 미확정 사항 3건을 §9 리스크에 추가 | — |
| 2026-07-02 | v0.5 | `HR_EMPL_ROLE_REL` 테이블을 Phase 2 데이터 모델 범위에 포함 확정 (관계자 확인 완료) — 로드맵 전체의 "15개 테이블" 표현을 "16개 테이블"로 정정 (§4 Phase 2/3, §11 데이터베이스·백엔드 체크리스트), §9 해당 리스크 항목 "해결" 처리, `backend/docs/ERD.md`에 §3.6-1 `HR_EMPL_ROLE_REL` 스키마 섹션 추가 | — |
| 2026-07-02 | v0.6 | `HR_SKILL_MST` 초기 Seed MVP 초안 작성(55건, 6개 그룹) 및 §9 리스크 "직원 기술 스택 표준화 기준 미정" 상태를 "차단→주의"로 하향 — 운영팀 최종 확정 전까지 MVP 표기 유지, §11 데이터베이스 체크리스트에 항목 추가 (미완료 유지) | — |
| 2026-07-02 | v0.7 | `SYS_ROLE_MST` 초기 Seed MVP 확정(ROLE_CD 6종, ROLE_NM/ROLE_DESC/화면 단위 `PERM_JSON`) — `backend/app/db/seed/sys_role_mst_seed.py` 작성, `backend/docs/ERD.md` §3.13 갱신. §9 리스크 "인증/권한 범위 미정", "`SYS_ROLE_MST` 세부 값 미정" 2건 "해결(MVP)"로 처리 | — |
| 2026-07-02 | v0.8 | MVP 권한 매트릭스(화면 접근 + 버튼 권한 조회/등록/수정/삭제/Excel/관리자 기능) 작성 — `backend/docs/PERMISSION_MATRIX.md` 신규, `sys_role_mst_seed.py`의 `PERM_JSON`을 화면×버튼 세부 구조(v2)로 갱신. §9 리스크 2건 해결 내용을 v2 매트릭스 기준으로 갱신 | — |
| 2026-07-03 | v0.9 | 가동 가능일 MVP 산정 기준 확정 — `backend/docs/AVAILABILITY_CALC_SPEC.md` 신규 작성(기준일/집계조건/`PROPOSED` 제외/3단계 산정식/100% 초과 예외 처리). §9 리스크 "가동 가능일 계산 기준 미정" 상태를 "차단→주의"로 하향, §4 Phase 5·§5 기능별 구현상태·§11 검색추천 체크리스트에 산정 기준 요약 반영 | — |
| 2026-07-03 | v1.0 | §8 다음 작업 4번(Alembic `env.py` 설정) 완료 처리 — `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/script.py.mako`, `backend/app/db/base.py` 작성. Phase 2 진행률 5%→10%로 갱신. §11 데이터베이스 체크리스트 "Alembic 마이그레이션 환경 구성" 항목 완료 처리. 실 DB 연결 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v1.1 | 전 컨테이너(api/web/worker/db/redis) 타임존 Asia/Seoul(KST) 통일 — `docker-compose.yml`에 `TZ`/`PGTZ` 환경변수 및 `/etc/localtime`·`/etc/timezone` 읽기전용 바인드 마운트 적용(YAML anchor 사용). `[DESIGN]HRM_Automation_System_Design_v0_6.md` §8.3 동일 갱신 및 §8.3-1(타임존 정책/Alpine tzdata 참고/운영 검증 명령) 신규 추가 — 예외적으로 운영 환경 구성 부분만 수정, 업무/DB/화면/API 설계는 변경 없음. §4 Phase 1 작업 목록에 타임존 통일 항목 추가 | — |
| 2026-07-03 | v1.2 | §9 리스크 및 차단 이슈 표 구조 변경 — `처리일자` 컬럼 신규 추가. `상태` 열에 섞여 있던 날짜·부가 설명(예: "해결 (MVP, 2026-07-02 갱신)", "주의 (2026-07-03 하향, 기존 차단)")을 `상태`(차단/주의/정상/해소/보류 단일 값)와 `처리일자`(`YYYY-MM-DD` 또는 미처리 시 `-`)로 분리. 상태값 표기를 "해결"→"해소"로 통일(대응 방안 본문 내 동일 표현 포함). 이슈·대응 방안의 실질 내용은 변경하지 않음 | — |
| 2026-07-03 | v1.3 | §8 다음 작업 5번(핵심 7개 테이블 생성) 완료 처리 — `backend/app/models/`에 SQLAlchemy 2.x ORM 모델 7종 및 공통 Mixin(`mixins.py`) 신규 작성, Alembic 리비전 `28ce52377e32_create_core_hr_pjt_tables.py` 수기 작성(로컬 `alembic` 패키지 미설치로 autogenerate 불가). Phase 2 진행률 10%→45%로 갱신. §11 데이터베이스 체크리스트에 완료 7개 테이블 체크 표시(전체 16개 중 7개, 부분 완료). 실 DB 적용 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v1.4 | §8 다음 작업 6번(`SYS_USER_MST`/`SYS_ROLE_MST`/`SYS_AUDIT_LOG` 테이블 생성 및 Seed 입력) 완료 처리 — 모델 3종 신규 작성, Alembic 리비전 `83fc676b952e_create_sys_user_role_audit_tables.py`(이전 리비전 뒤 체이닝)에 `SYS_ROLE_MST` 6종 Seed(`op.bulk_insert`, 기존 `sys_role_mst_seed.py` 재사용) 포함 작성. Phase 2 진행률 45%→60%로 갱신. §11 데이터베이스 체크리스트에 완료 3개 테이블 체크(전체 16개 중 10개) 및 Seed 항목 부분 완료(HR_JIKGUP_MST/HR_JIKMU_MST Seed 미작성) 반영. 실 DB 적용 검증은 로컬 환경 제약으로 미실시 | — |

