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
| Phase 1 | 인프라 및 개발환경 구축 | 2주차 | 완료 | 100% | 정상 |
| Phase 2 | PostgreSQL 데이터 모델 구축 | 2~3주차 | 완료 | 100% | 정상 |
| Phase 3 | FastAPI 백엔드 구축 | 3~5주차 | 완료 | 100% | 정상 |
| Phase 4 | Next.js 웹 클라이언트 구축 | 3~5주차 | 진행 중 | 50% | 정상 |
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
| **개발 상태** | 완료 |
| **진행률** | 100% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| Ubuntu Server 24.04 LTS 환경 준비 | 완료 |
| Docker Engine 설치 | 완료 |
| Docker Compose Plugin 설치 | 완료 (v2 플러그인 전환, `Docker Compose version v5.2.0` 확인, 2026-07-03) |
| `/App/hrmngr/` 디렉토리 구조 생성 | 완료 (`backend/`, `frontend/`, `data/postgres/`, `data/redis/`, `backup/postgres/`, `logs/`) |
| `docker-compose.yml` 초안 작성 (api / web / db / redis / worker) | 완료 (`docker-compose config`로 문법 검증 완료) |
| 전 컨테이너 타임존 KST(Asia/Seoul) 통일 | 완료 (2026-07-03 — `TZ`/`PGTZ` 환경변수 + `/etc/localtime`·`/etc/timezone` 읽기전용 바인드 마운트, YAML anchor로 중복 최소화. 실 컨테이너 기동 후 `date`/`SHOW timezone;` 검증은 서버에서 수행 필요) |
| `.env` 파일 작성 및 `.gitignore` 설정 | 완료 (`.env.example` 작성, `.gitignore`에 `data/`, `backup/postgres/*.sql.gz`, `logs/`, `.next/` 추가) |
| Git Repository 초기화 | 완료 (기존 리포지토리) |
| PostgreSQL 컨테이너 기동 및 포트 5442 접속 확인 | 완료 (컨테이너 `Healthy`, `alembic upgrade head`로 DB 연결·쿼리 확인. 외부 노출은 `127.0.0.1:5442`로 제한 — `docker-compose.yml` 반영, 2026-07-03) |
| FastAPI 컨테이너 기동 및 `/health` 응답 확인 | 완료 (`curl http://localhost:8000/health` → `{"status":"ok"}` 확인, 2026-07-03) |
| Next.js 컨테이너 기동 및 포트 3030 접속 확인 | 완료 (`curl -I http://localhost:3030` → `307 → /dashboard` 정상 확인, 2026-07-03) |
| 방화벽(UFW) 설정 (3030, 8000 허용 / 5442 내부망 제한) | 완료 (22/3030/8000 UFW 허용 및 활성화, 5442는 `docker-compose.yml`에서 `127.0.0.1:5442:5432`로 바인딩해 애초에 외부 인터페이스로 노출되지 않도록 처리 — Docker가 UFW 규칙보다 우선하는 자체 iptables 규칙을 추가하는 문제를 우회, 2026-07-03) |

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
| **개발 상태** | 완료 |
| **진행률** | 100% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| ERD 최종 확정 | 완료 (`backend/docs/ERD.md`, 2026-07-02) |
| Alembic 마이그레이션 환경 구성 | 완료 (`backend/alembic.ini`, `backend/alembic/env.py`, 2026-07-03 — 실 서버에서 `alembic upgrade head` 적용 검증 완료, 2026-07-03) |
| `HR_DEPT_MST` (부서 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_JIKGUP_MST` (직급 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_JIKMU_MST` (직무 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_SKILL_MST` (기술 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_EMPL_MST` (사원 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_EMPL_SKILL_REL` (사원기술 연결) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_EMPL_ROLE_REL` (사원역할 연결, 복수 직무 지원) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `PJT_MST` (프로젝트 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `PJT_ASGN_HIS` (투입 이력) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `PJT_RSRC_REQ` (리소스 요청) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `PJT_RCMD_RSLT` (추천 결과) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `HR_AVAIL_SNAP` (가동가능 스냅샷) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `SYS_USER_MST` (사용자 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `SYS_ROLE_MST` (역할 마스터) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `SYS_AUDIT_LOG` (감사 로그) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| `SYS_BATCH_HIS` (배치 이력) 테이블 생성 | 완료 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| Seed 데이터 입력 (`SYS_ROLE_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST` 12종) | 완료 (3종 전부 실 서버 DB 삽입 검증 완료 — `SYS_ROLE_MST` 6건/`HR_JIKGUP_MST` 10건/`HR_JIKMU_MST` 12건 `SELECT COUNT(*)` 확인, 2026-07-03) |
| DB 백업 스크립트 작성 및 crontab 등록 (매일 02:00) | 완료 (Phase 2 범위) — 스크립트(`backup/backup_db.sh`)는 Phase 1에서 작성, 2026-07-03 실 서버에서 수동 실행해 `pg_dump` 백업 파일 정상 생성 확인(`hrm_20260703_132344.sql.gz`, `CREATE TABLE` 17건 포함) — Phase 2 완료 기준 충족. crontab 자동 등록(매일 02:00)은 별도 배치 운영 항목(`SYS_DB_BACKUP`)으로 §4 Phase 7·§11에 이미 반영되어 있어 그쪽에서 마무리 |

**산출물**

- Alembic 마이그레이션 스크립트 (전체 테이블)
- Seed 데이터 SQL 또는 Python 스크립트
- `backup_db.sh`

**완료 기준**

- `alembic upgrade head` 실행 후 16개 테이블 전부 생성 확인 — ✅ 충족 (2026-07-03, `\dt` 결과 16개 테이블 + `alembic_version` 확인)
- Seed 데이터 정상 입력 확인 — ✅ 충족 (2026-07-03, `SYS_ROLE_MST` 6건/`HR_JIKGUP_MST` 10건/`HR_JIKMU_MST` 12건 `SELECT COUNT(*)` 확인)
- `pg_dump` 백업 파일 생성 확인 — ✅ 충족 (2026-07-03, `backup_db.sh` 수동 실행으로 `hrm_20260703_132344.sql.gz` 생성 확인. 단, crontab 자동화(매일 02:00)는 별도 미완료 항목 — §11 참조)

---

### Phase 3. FastAPI 백엔드 구축

| 항목 | 내용 |
|---|---|
| **목표** | 핵심 업무 도메인 REST API 구현 및 인증·권한·감사 로그 적용 |
| **계획 기간** | 3~5주차 |
| **개발 상태** | 완료 (2026-07-03 — "완료 기준" 4개 항목 전부 충족) |
| **진행률** | 100% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| FastAPI 프로젝트 기본 구조 생성 (`app/`, `models/`, `schemas/`, `api/v1/`) | 완료 (Phase 1~2에서 기본 골격 구성, `api/v1/router.py` 신규 추가로 라우터 등록 구조 확립, 2026-07-03) |
| SQLAlchemy 2.x ORM 모델 작성 (16개 테이블) | 완료 (16/16, Phase 2 완료로 전체 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03) |
| Pydantic v2 스키마 작성 | 완료 (16개 테이블 전체 조회(Out) 스키마 작성, 실 서버 컨테이너에서 실제 임포트 및 ORM 데이터 검증 완료, 2026-07-03 — `EmployeeCreate`/`EmployeeUpdate` 등 등록/수정 스키마는 각 CRUD API 구현 시 추가 예정) |
| `/health` 헬스체크 엔드포인트 구현 | 완료 (Phase 1, `backend/app/main.py`) |
| JWT 인증 API 구현 (`SYS_USER_MST` 기반) | 완료 (로그인/토큰 갱신/로그아웃 구현 — `POST /api/v1/auth/{login,refresh,logout}`, 실 서버 컨테이너 재빌드 후 curl 검증 완료, 2026-07-03. 로그아웃은 stateless 토큰 특성상 서버 측 즉시 무효화는 미구현 — 하단 비고 참조) |
| RBAC 권한 미들웨어 구현 (`SYS_ROLE_MST` 기반) | 완료 (인증 의존성 `get_current_user`, 화면×버튼 권한 검사 `require_permission` 구현 및 `employees`/`skills`/`employee-skills`/`projects`/`assignments`/`codes`(부서·직급·직무유형, `codes` 공통 권한 키 신규) 6개 라우터 전체에 적용, 실 서버 curl 검증 완료, 2026-07-03 — 인증 없이 호출 가능한 업무 API는 더 이상 없음) |
| `SYS_AUDIT_LOG` 감사 로그 미들웨어 구현 | 완료 (로그인 및 5개 라우터(`employees`/`skills`/`employee-skills`/`projects`/`assignments`)의 등록/수정 행위 기록 구현, 실 서버 검증 완료, 2026-07-03. 조회(GET) 감사 로그 조회 API는 별도 미구현) |
| CORS 설정 (포트 3030 허용) | 완료 (Phase 1, `backend/app/main.py`) |
| 사원 CRUD API (`HR_EMPL_MST`) | 완료 (조회/등록/수정/퇴직 처리 구현 — `GET`/`POST`/`PATCH`/`DELETE /api/v1/employees`, `DELETE`는 로우 삭제가 아닌 `EMPL_STAT_CD='RETIRED'` 전환, 실 서버 검증 완료, 2026-07-03) |
| 부서/직급/직무 코드 API (`HR_DEPT_MST`, `HR_JIKGUP_MST`, `HR_JIKMU_MST`) | 완료 (조회 API만 구현 — `GET /api/v1/departments`, `/positions`, `/job-types`, 2026-07-03. 등록/수정은 §11 "직무 유형 CRUD API" 항목으로 별도 관리) |
| 기술 CRUD API (`HR_SKILL_MST`, `HR_EMPL_SKILL_REL`) | 완료 (조회/등록/수정 구현 — `GET`/`POST`/`PATCH /api/v1/skills`, `/api/v1/employee-skills`, 실 서버 컨테이너 재빌드 후 curl 검증 완료, 2026-07-03) |
| 프로젝트 CRUD API (`PJT_MST`) | 완료 (조회/등록/수정 구현 — `GET`/`POST`/`PATCH /api/v1/projects`, 실 서버 컨테이너 재빌드 후 curl 검증 완료, 2026-07-03) |
| 투입 관리 API (`PJT_ASGN_HIS`) | 완료 (조회/등록/수정 구현 — `GET`/`POST`/`PATCH /api/v1/assignments`, 동일 사원·겹치는 기간 ALLOC_RT 합계 100% 초과 검증 포함, 실 서버 컨테이너 재빌드 후 curl 검증 완료, 2026-07-03) |
| 가동률 계산 API (`HR_AVAIL_SNAP`) | 완료 (`GET /api/v1/availability/{empl_id}` — `AVAILABILITY_CALC_SPEC.md` §2/§4 로직으로 즉시 계산, `HR_AVAIL_SNAP` 테이블에는 저장하지 않음(스냅샷 저장은 Phase 7 배치 `HR_AVAIL_SNAP_GEN` 전담), 실 서버 검증 완료, 2026-07-03) |
| 대시보드 집계 API | 완료 (SCR-002 설계서 명시 4개 + 프론트엔드 목데이터 기반 4개, 총 8개 엔드포인트 — `GET /api/v1/dashboard/{summary,dept-utilization,job-type-distribution,utilization-by-type,data-quality,ending-this-month,recent-employees,headcount-trend}` 구현, 실 서버 검증 완료, 2026-07-03. `HR_AVAIL_SNAP` 배치 미구현으로 실시간 계산 로직으로 대체 — 하단 비고 참조) |
| Excel Import/Export API | 완료 (`GET /api/v1/employees/export` + `POST /api/v1/employees/import`, SCR-003 "인력마스터_ResourceTable" 컬럼 매핑 그대로 구현, 실 서버 검증 완료, 2026-07-03. Import 정책: 마스터 미존재 시 전체 실패, `EMPL_NO` 기준 Upsert, 일부 실패 시 전체 롤백 — 사용자 확정, 하단 비고 참조) |
| 페이지네이션 공통 처리 구현 | 완료 (`app/core/pagination.py`(`PaginationParams`), `app/schemas/pagination.py`(`PaginatedResponse` 제네릭)로 추출, `employees`/`projects`/`assignments` 3개 라우터 적용, 실 서버 검증 완료, 2026-07-03) |
| OpenAPI 문서 확인 (`/docs`) | 완료 (실 서버 `/docs`·`/redoc`·`/openapi.json` 정상 응답 확인, 22개 엔드포인트 전부 태그·설명·응답 코드 정상 노출, `HTTPBearer` 보안 스키마 자동 반영 확인, 2026-07-03) |

**산출물**

- FastAPI 앱 전체 소스 (`/App/hrmngr/backend/`)
- OpenAPI 문서 (`/docs`, `/redoc`)

**완료 기준**

- 핵심 CRUD 엔드포인트 전부 응답 확인 (Postman 또는 `/docs` 기준) — ✅ 충족 (실 서버 `curl` 검증, §7 각 항목 참조)
- JWT 인증·RBAC 권한 필터 동작 확인 — ✅ 충족 (2026-07-03)
- `SYS_AUDIT_LOG` 변경 이력 기록 확인 — ✅ 충족 (2026-07-03)
- Pytest 단위 테스트 핵심 API 커버 — ✅ 충족 (2026-07-03, `backend/tests/`에 16개 테스트 작성 — health/인증(로그인 성공·실패·토큰 갱신·토큰 타입 검증)/RBAC(권한 없음 403·조회 허용)/사원 CRUD(생성·조회·수정·퇴직·중복 409)/투입 관리(ALLOC_RT 100% 초과 검증·취소 건 제외) 커버, 실 서버 컨테이너에서 `pytest` 실행 결과 16개 전부 통과 확인)

**Phase 3 완료 (2026-07-03)** — 위 4개 완료 기준 전부 충족되어 Phase 3을 정식으로 완료 처리한다.

---

### Phase 4. Next.js 웹 클라이언트 구축

| 항목 | 내용 |
|---|---|
| **목표** | 권한별 메뉴 제어가 적용된 웹 화면 전체 구현 (포트 3030) |
| **계획 기간** | 3~5주차 |
| **개발 상태** | 진행 중 |
| **진행률** | 50% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| Next.js 프로젝트 생성 (`output: 'standalone'`) | 완료 (Phase 1, `frontend/next.config.mjs`) |
| `NEXT_PUBLIC_API_BASE_URL` 환경변수 설정 | 완료 (Phase 1, `.env.example`. 2026-07-03: Docker 빌드 시 이 값이 클라이언트 번들에 실제로 주입되지 않던 버그 발견 및 수정 — 하단 비고 참조) |
| 로그인 화면 구현 (`/login`) | 완료 (`frontend/app/login/page.tsx`, 기존 스캐폴딩 보강 — JWT API 전까지 `lib/auth.ts` MVP 세션 마커로 대체, 2026-07-03) |
| 로그인 JWT API 연동 (`frontend/lib/auth.ts` localStorage 임시 마커 → `POST /api/v1/auth/{login,refresh,logout}` 실 API 연동) | 완료 (`lib/auth.ts`에 `login`/`logout`/`getAccessToken` 추가, `login/page.tsx`·`top-nav.tsx` 실 API 연동, 실 서버 컨테이너 빌드·번들 검증 완료, 2026-07-03. 토큰 저장은 MVP로 localStorage 유지 — HttpOnly Cookie 전환은 별도 후속 과제) |
| 공통 레이아웃·네비게이션 구현 (권한별 메뉴 제어) | 완료 (레이아웃·네비게이션·미인증 리다이렉트 및 `SYS_ROLE_MST.PERM_JSON` 기반 사이드바 메뉴 필터링 구현, 실 서버 검증 완료, 2026-07-03) |
| 대시보드 화면 구현 (`/dashboard`) — 직무 유형 분포 위젯 포함 | 완료 (목데이터를 백엔드 8개 API로 전량 교체, 실 서버 빌드·번들 검증 완료, 2026-07-03) |
| 사원 목록 화면 구현 (`/employees`) — 직무 유형 필터 포함 | 완료 (기존 스캐폴딩 + 직무 유형 필터 추가, 목데이터 기반, 2026-07-03) |
| 사원 상세 화면 구현 (`/employees/[id]`) | 완료 (기존 목데이터 기반 스캐폴딩을 백엔드 실 API로 연동 — 기본정보/보유기술/투입이력 3개 탭 실 데이터 조회, 신규 `GET /api/v1/employees/{empl_id}` 추가, 실 서버 빌드·검증 완료, 2026-07-03. 정보수정/기술추가/퇴직처리 버튼은 조회 전용으로 남기고 후속 작업으로 분리 — §9 참조) |
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
| 직원 관리 | `HR_EMPL_MST` CRUD, 퇴직 처리 | 완료 (조회/등록/수정/퇴직 처리 구현, 실 서버 검증 완료 — 2026-07-03) | 높음 | `employees.py`, `HR_EMPL_MST` | 직무 유형(`JIKMU_ID`) 필드 포함 |
| 팀/조직 관리 | `HR_DEPT_MST` 계층 구조 관리 | 진행 중 (조회 API만 구현 — `GET /api/v1/departments`, 등록/수정/계층 구조 관리 미구현) | 높음 | `codes.py`, `HR_DEPT_MST` | 상위 부서(`PRNT_DEPT_ID`) 지원 |
| 직급/역할 관리 | `HR_JIKGUP_MST`, `HR_JIKMU_MST` 마스터 관리 | 진행 중 (조회 API만 구현 — `GET /positions`, `/job-types`, 등록/수정 미구현) | 높음 | `codes.py` | 직급·직무 분리 설계 |
| 기술 스택 관리 | `HR_SKILL_MST` CRUD | 완료 (조회/등록/수정 구현, 실 서버 검증 완료 — 2026-07-03) | 높음 | `skills.py`, `HR_SKILL_MST` | 기술 그룹(`SKILL_GRP_CD`) 분류 |
| 직원별 숙련도 관리 | `HR_EMPL_SKILL_REL` 등록·수정 | 완료 (조회/등록/수정 구현, 실 서버 검증 완료 — 2026-07-03) | 높음 | `employee_skills.py`, `HR_EMPL_SKILL_REL` | `PRFCY_LEVL` 1~5 |
| 프로젝트 관리 | `PJT_MST` CRUD, 상태 관리 | 완료 (조회/등록/수정 구현, 실 서버 검증 완료 — 2026-07-03) | 높음 | `projects.py`, `PJT_MST` | `PJT_STAT_CD` (PLANNED/RUNNING/CLOSED/HOLD) |
| 프로젝트 투입 관리 | `PJT_ASGN_HIS` 등록·수정·취소 | 완료 (조회/등록/수정 구현, 취소는 `PATCH`로 `ASGN_STAT_CD='CANCELED'` 전환, 실 서버 검증 완료 — 2026-07-03) | 높음 | `assignments.py`, `PJT_ASGN_HIS` | 투입 역할(`PRJT_ROLE_NM`) 포함 |
| 투입률 관리 | `ALLOC_RT` 합계 검증 및 표시 | 완료 (동일 사원·겹치는 기간 유효(`PLANNED`/`ACTIVE`) 투입 합계 100% 초과 시 409 거부 구현, 실 서버 검증 완료 — 2026-07-03) | 높음 | `assignments.py`, `pjt_asgn_his.py`(repository) | 동일 기간 합계 100% 초과 방지 |
| 종료 예정일 관리 | `ASGN_END_DT` 조회·알림 | 예정 | 높음 | `PJT_ASGN_HIS`, `PJT_ASGN_END_ALERT` 배치 | 30일 이내 종료 예정 알림 |
| 가동 가능일 자동 계산 | `HR_AVAIL_SNAP` 기반 산정 | 진행 중 (즉시 계산 API `GET /api/v1/availability/{empl_id}` 구현 완료, 2026-07-03 — 매일 01:00 자동 스냅샷 생성 배치 `HR_AVAIL_SNAP_GEN`은 Phase 7 미구현) | 높음 | `availability.py`, `HR_AVAIL_SNAP_GEN` 배치 | 투입률 0%=AVAILABLE(기준일), 1~99%=PARTIAL(기준일), ≥100%=FULL(MAX(종료일)+1, 종료일 NULL 시 품질경고) — `PROPOSED` 제외, 상세는 `backend/docs/AVAILABILITY_CALC_SPEC.md` |
| 즉시 투입 가능 인력 조회 | `AVAIL_STAT_CD='AVAILABLE'` 필터 | 예정 | 높음 | `GET /api/v1/availability` | 직무 유형 필터 포함 |
| 기술 기반 인력 검색 | 기술·숙련도·직무 복합 검색 | 예정 | 높음 | `recommendations.py` | `HR_EMPL_SKILL_REL` + `HR_JIKMU_MST` 조인 |
| 프로젝트 종료 예정자 조회 | 이번 달/30일 이내 종료 예정자 | 예정 | 높음 | `reports.py`, `PJT_ASGN_HIS` | |
| 팀별 가동률 조회 | 부서별 평균 `TOT_ALLOC_RT` | 예정 | 중간 | `dashboard.py`, `HR_AVAIL_SNAP` | |
| 리소스 추천 | `PJT_RCMD_RSLT` 점수 기반 후보 추천 | 예정 | 중간 | `recommendation_service.py` | 6개 항목 가중 점수 |
| AI 질의응답 | 자연어 → 조건 파싱 → SQL 조회 → 요약 | 예정 | 중간 | `ai_service.py`, `POST /api/v1/ai/chat` | Phase 6 |
| 주간 리포트 | `PJT_WEEKLY_RPT` 자동 발송 | 예정 | 중간 | `report_service.py`, Teams Webhook | 매주 월요일 09:00 |
| 감사 로그 | `SYS_AUDIT_LOG` 변경 이력 기록 | 완료 (로그인 및 5개 라우터의 등록/수정 행위 기록 구현, 실 서버 검증 완료 — 2026-07-03. Import 등 미구현 기능 관련 로그, 조회 API는 별도) | 높음 | `sys_audit_log.py`, `app/core/audit.py` | 로그인·CRUD·Import 포함 |
| 사용자 인증/권한 | JWT + RBAC (`SYS_USER_MST`, `SYS_ROLE_MST`) | 완료 (JWT 로그인/토큰갱신/로그아웃 및 RBAC 전 라우터(`employees`/`skills`/`employee-skills`/`projects`/`assignments`/`codes`) 적용 완료 — 2026-07-03) | 높음 | `auth.py`, `security.py`, `deps.py` | 6개 역할 |
| 백업/복구 | `SYS_DB_BACKUP` 자동화, `pg_dump` | 진행 중 (수동 백업 스크립트 작성 및 실행 확인 완료, crontab 자동화·복구 테스트 미완료) | 높음 | `backup_db.sh`, crontab | 매일 02:00, 14일 보관 |
| 배포 자동화 | Docker Compose 기반 배포 | 완료 (실 서버에서 `docker compose`로 api/web/db/redis/worker 5개 서비스 정상 구동 중 — 2026-07-03) | 높음 | `docker-compose.yml` | CI/CD는 확장 단계 |

---

## 6. 기술 구성 요소별 진행 상태

| 구성 요소 | 적용 기술 | 상태 | 필수 여부 | 비고 |
|---|---|---|---|---|
| Ubuntu Server | Ubuntu 24.04 LTS | 적용 완료 | 필수 | 운영 서버 OS, 실 서버 구축 확인 완료 (2026-07-03) |
| Docker | Docker Engine (최신) | 적용 완료 | 필수 | 컨테이너 런타임, `sg docker`로 `novauser` 권한 확인 후 직접 운용 중 |
| Docker Compose | Docker Compose Plugin v2 | 적용 완료 (v5.2.0) | 필수 | 멀티 컨테이너 오케스트레이션, 5개 서비스 정상 구동 확인 (2026-07-03) |
| PostgreSQL | PostgreSQL 16-alpine (Docker) | 적용 완료 | 필수 | 외부 포트 `127.0.0.1:5442`(보안 조치 반영), 데이터 `/App/hrmngr/data/postgres/`, 16개 테이블 정상 구동 확인 (2026-07-03) |
| FastAPI | FastAPI + Uvicorn (Python 3.12) | 적용 완료 | 필수 | 포트 8000, `/health` 및 다수 API 정상 응답 확인. 운영 시 Gunicorn+Uvicorn Worker 전환은 미검토 |
| SQLAlchemy 또는 SQLModel | SQLAlchemy 2.x + Alembic | 적용 완료 | 필수 | ORM 및 마이그레이션, 16개 테이블 모델 작성 및 실 DB 적용 완료 |
| Alembic | Alembic (SQLAlchemy 연동) | 적용 완료 | 필수 | DB 스키마 버전 관리, 실 서버 `alembic upgrade head` 정상 실행 확인 |
| Next.js | Next.js (node:22-alpine, standalone) | 진행 중 | 필수 | 외부 포트 3030, `output: 'standalone'` 적용·컨테이너 구동 확인. 대부분 화면은 목데이터 기반이라 실 API 연동은 미완료 |
| API Client | Axios 또는 fetch (Next.js 내장) | 진행 중 | 필수 | 로그인 화면은 `fetch` 기반으로 실 API(`/api/v1/auth/*`) 연동 완료(2026-07-03). 나머지 화면들은 여전히 목데이터 사용 중이라 연동 미착수. `NEXT_PUBLIC_API_BASE_URL`이 Docker 빌드 시 클라이언트 번들에 주입되지 않던 버그를 함께 수정(하단 §9 참조) |
| 인증 방식 | JWT (Access Token 60분 + Refresh Token 7일) | 진행 중 | 필수 | 백엔드 로그인/토큰갱신/로그아웃 API 구현 및 검증 완료, 프론트엔드도 `lib/auth.ts`가 실제 로그인/로그아웃 API를 호출하도록 연동 완료(2026-07-03) — 단, 토큰 저장은 MVP로 localStorage 유지, 설계서가 목표로 하는 HttpOnly Cookie·Token Rotation·자동 리프레시는 아직 미구현 |
| Batch/Scheduler | APScheduler (MVP) → Celery (확장) | 예정 | 필수 | `hrm-worker` 컨테이너는 Phase 7까지 placeholder로 구동 중(실제 배치 로직 없음) |
| Logging | structlog 또는 Python logging (JSON 포맷) | 예정 | 필수 | `/App/hrmngr/logs/`, 현재 기본 Uvicorn 로그만 사용, 구조화 로그 미적용 |
| Backup | `pg_dump` + gzip + crontab | 진행 중 | 필수 | `/App/hrmngr/backup/postgres/`, 수동 백업 스크립트 작성·실행 확인 완료(2026-07-03), crontab 자동화·14일 보관 정책은 미완료 |
| Nginx | Nginx (선택) | 예정 | 선택 | 초기 구축에서는 제외 가능하며, HTTPS/도메인/운영 안정화 단계에서 추가 검토 |
| AI Agent / LLM 연동 | OpenAI API 또는 Anthropic API (MVP), 사내 LLM (확장) | 예정 | 선택 | Phase 6, LLM 호출 레이어 추상화 필수 |
| Redis | Redis 7-alpine (Docker) | 진행 중 | 선택 | 컨테이너(`hrm-redis`)는 정상 구동 중이나 애플리케이션 코드에서 아직 연동(캐시/큐 등)하지 않음 — MVP에서 생략 가능한 범위 |

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
- (§8 다음 작업 7번) 사원 목록 조회 API 구현(`GET /api/v1/employees`) — `backend/app/db/session.py`(SQLAlchemy 동기 세션·`get_db` 의존성 신규 작성, 기존 `DATABASE_URL` 설정 재사용), `backend/app/schemas/hr_empl_mst.py`(`EmployeeOut`/`EmployeeListResponse`), `backend/app/repositories/hr_empl_mst.py`(부서/직무 유형/재직상태 필터 + skip/limit 페이지네이션 쿼리, 화면 설계서 SCR-003 직무 유형 필터 요건 반영), `backend/app/api/v1/employees.py`(라우터) 신규 작성. 향후 엔드포인트 추가에 대비해 `backend/app/api/v1/router.py`(API 라우터 집합)를 신규 도입하고 `backend/app/main.py`에 `/api/v1` prefix로 등록. 공통 페이지네이션 유틸리티(로드맵 §11 "페이지네이션 공통 처리 구현")는 아직 별도 구현하지 않고 이 엔드포인트에 한해 skip/limit을 직접 적용 — 향후 재사용 필요 시 별도 모듈로 추출 예정. **실 서버 기동 후 엔드포인트 호출 검증은 로컬 환경에 `fastapi`/`pydantic`/`sqlalchemy` 미설치로 미실시** — 모델·스키마 필드 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- (§8 다음 작업 8번) 사원 등록/수정 API 구현(`POST`, `PATCH /api/v1/employees`) — `backend/app/schemas/hr_empl_mst.py`에 `EmployeeCreate`/`EmployeeUpdate` 추가(`EMPL_STAT_CD`는 모델의 `EMPL_STAT_CODES` 상수를 그대로 재사용해 `Literal` 타입으로 검증, DB CHECK 제약과 값 목록이 어긋나지 않도록 함), `backend/app/repositories/hr_empl_mst.py`에 `get_employee`/`create_employee`/`update_employee` 추가, `backend/app/api/v1/employees.py`에 `POST /api/v1/employees`(201 Created), `PATCH /api/v1/employees/{empl_id}`(부분 업데이트, 미존재 시 404) 라우터 추가. `EMPL_NO`/`EMAIL_ADDR` UNIQUE 위반 및 `DEPT_ID`/`JIKGUP_ID`/`JIKMU_ID` FK 위반은 `IntegrityError`를 잡아 409로 변환. **부분 완료**: 퇴직 처리(DELETE, `EMPL_STAT_CD='RETIRED'` 전환)는 §8 목록에 없어 이번 범위에서 제외 — 사원 CRUD API는 계속 "진행 중" 유지. JWT 인증·RBAC·`SYS_AUDIT_LOG` 감사 로그 연동은 미구현(§8 목록에 아직 없는 별도 작업). **실 서버 기동 후 엔드포인트 호출 검증은 로컬 환경 제약으로 미실시** — 모델-스키마 필드 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- (§8 다음 작업 9번) Next.js 기본 레이아웃 구성(로그인 화면, 공통 네비게이션) — `frontend/app/(app)/`, `app/login/page.tsx`, `components/layout/{app-shell,sidebar,top-nav}.tsx` 등 기존 스캐폴딩(로그인 폼·사이드바·상단바)이 이미 존재함을 확인, 다만 로그인 성공 후 세션이 전혀 저장되지 않고 미인증 상태에서도 모든 화면에 접근 가능한 상태였음. 이를 실제로 동작하는 흐름으로 연결하기 위해 `frontend/lib/auth.ts`(신규)를 추가 — JWT 인증 API(§4 Phase 3)가 아직 없어 localStorage 기반 임시 세션 마커로 대체하며, 파일 상단 주석에 임시 처리 사유와 교체 필요성을 명시. 로그인 성공 시 `setAuthenticated()` 호출(`login/page.tsx`), `AppShell`에 미인증 시 `/login`으로 리다이렉트하는 가드 추가(`app-shell.tsx`), 로그아웃 시 `clearAuthenticated()` 호출(`top-nav.tsx`). Next.js 프로젝트 생성·`NEXT_PUBLIC_API_BASE_URL` 설정은 Phase 1에서 이미 완료되어 있었음을 확인해 §4/§11 반영. **미완료로 남긴 부분**: "권한별 메뉴 제어"(사이드바 메뉴를 `SYS_ROLE_MST.PERM_JSON` 기준으로 필터링하는 기능)는 로그인 API·현재 사용자 컨텍스트가 없어 이번 범위에서 구현하지 않음 — §11 프론트엔드 체크리스트에 미완료로 유지. **Next.js 빌드/타입체크는 로컬 환경에 `node_modules` 미설치 및 Node 버전(v16, 프로젝트 요구 Node 20+)이 낮아 미실행**
- (§8 다음 작업 10번) 사원 목록 화면 구현(`/employees` — 직무 유형 필터 포함) — `frontend/app/(app)/employees/page.tsx`에 검색/조직/직급/재직상태 필터, 테이블, 등록 모달이 이미 스캐폴딩되어 있었으나, "직무 유형" 필터가 없고 대신 `HR_JIKMU_MST` 마스터와 무관한 하드코딩된 "보유 역할" 목록(`roleOptions`)을 사용 중이었음을 확인. 기존에 있던 `jobTypeOptions`(`lib/options.ts`, `HR_JIKMU_MST` 마스터 기준, `/recommendations`·`/availability`에서 이미 사용 중)를 재사용해 필터를 "직무 유형"으로 교체. 사원 mock 데이터의 `roles` 필드에 신규 JIKMU_CD(`DEVELOPER` 등)와 구 Excel 코드(`AA`/`TA`/`컨설턴트`/`사업관리`)가 혼재되어 있어(ERD `HR_JIKMU_MST` §3.3 매핑 규칙과 동일한 현상) 필터가 두 표기 모두에서 정상 동작하도록 로컬 별칭 매핑(`JIKMU_CD_ALIASES`)을 페이지 파일 내에 추가하고 사유를 주석으로 명시. 테이블의 "보유 역할" 컬럼(다중 역할 배지 표시)은 필터와 별개 개념이라 변경하지 않음. **미완료로 남긴 부분**: 화면은 여전히 `lib/mock-data.ts` 목데이터 기반이며 `GET /api/v1/employees` 실 API 연동은 하지 않음 — §11 체크리스트에 명시. **Next.js 빌드/타입체크는 로컬 환경 제약(Node 16, `node_modules` 미설치)으로 미실행**
- **실 서버 배포 검증 및 버그 수정** — 사용자가 실 서버(Ubuntu 호스트)에서 Docker Compose Plugin v2(v5.2.0) 전환 및 UFW 방화벽(22/3030/8000 허용) 설정을 완료한 뒤 `docker compose up -d --build`~`alembic upgrade head`를 진행하는 과정에서 발견된 문제 4건을 수정:
  1. **`frontend` Docker 빌드 실패 (pnpm 버전 미고정)** — `corepack enable`이 pnpm 버전을 고정하지 않아 최신 pnpm 11.x를 받아왔고, `pnpm-lock.yaml`(`lockfileVersion: 9.0`)과 `overrides` 설정 위치가 pnpm 11에서 바뀌며 `ERR_PNPM_LOCKFILE_CONFIG_MISMATCH` 발생 → `frontend/package.json`에 `"packageManager": "pnpm@9.15.4"` 추가로 고정
  2. **`frontend` Docker 빌드 실패 (public 디렉토리 부재)** — `runner` 스테이지의 `COPY --from=builder /app/public ./public`이 실패(프로젝트에 `public/`가 아예 없었음) → `frontend/public/.gitkeep` 추가
  3. **`alembic upgrade head` 실행 시 `Name or service not known`** — 근본 원인은 DNS가 아니라 `.env`의 `DATABASE_URL`에 담긴 비밀번호에 URL 특수문자(`@`, `#`)가 인코딩되지 않고 그대로 들어가 URL 파싱이 깨진 것 — 사용자가 `.env`에서 percent-encoding 적용(`.env`는 원칙대로 직접 수정하지 않고 방법만 안내)
  4. **`alembic upgrade head` 실행 시 `invalid interpolation syntax`** — percent-encoding된 비밀번호의 `%` 문자를 Python `ConfigParser`(BasicInterpolation)가 보간 문법으로 오인 → `backend/alembic/env.py`에서 `config.set_main_option` 호출 시 `%`를 `%%`로 이스케이프하도록 수정 (Alembic 공식 권장 우회)
  5. **`CREATE TABLE` 실행 시 `column "empl_stat_cd" does not exist`** — `HR_EMPL_MST`/`PJT_MST`/`PJT_ASGN_HIS`의 `CheckConstraint` 원문 SQL에 컬럼명을 큰따옴표로 감싸지 않아, SQLAlchemy가 큰따옴표로 생성한 실제 컬럼(`"EMPL_STAT_CD"`)과 대소문자가 안 맞아 Postgres가 소문자로 접어 컬럼을 찾지 못함 → `backend/app/models/{hr_empl_mst,pjt_mst,pjt_asgn_his}.py`와 `backend/alembic/versions/28ce52377e32_...py`의 CHECK 제약 6곳 모두 컬럼명에 큰따옴표 추가
  - 수정 후 실 서버에서 **10개 테이블 생성 및 `SYS_ROLE_MST` 6종 Seed 삽입을 `\dt`/`SELECT`로 최종 확인 완료**. §8 4~6번, §11 데이터베이스 체크리스트의 "실 DB 미검증" 표기를 전부 "실 서버 DB 적용 검증 완료"로 갱신
- **Phase 1 완료 — 전체 컨테이너 헬스체크 및 5442 포트 보안 조치** — 사용자가 `curl http://localhost:8000/health` → `{"status":"ok"}`, `curl -I http://localhost:3030` → `307 Temporary Redirect → /dashboard` 정상 응답을 확인해 FastAPI/Next.js 컨테이너 기동 항목을 완료 처리. PostgreSQL 외부 노출 문제는 UFW 규칙이 아니라 `docker-compose.yml`의 `db` 서비스 포트 바인딩을 `"5442:5432"` → `"127.0.0.1:5442:5432"`로 변경해 해결 — Docker가 게시 포트에 대해 UFW보다 먼저 적용되는 자체 iptables 규칙을 추가하는 문제가 있어, UFW 규칙만으로는 외부 접근을 확실히 차단하지 못할 수 있다는 점을 코드 주석으로 명시. `POSTGRES_PASSWORD` 로테이션도 사용자가 즉시 완료. §3/§4 Phase 1을 "완료(100%)"로 전환, §9 리스크 2건(비밀번호 노출, UFW 5442) "해소" 처리. 포트 바인딩 변경 후 `docker compose up -d --force-recreate db`로 재생성해 `./data/postgres` 볼륨 데이터(11개 테이블, `SYS_ROLE_MST` 6종 Seed)가 유실 없이 그대로 유지됨을 재확인 완료
- **Phase 2 계속 — `HR_EMPL_SKILL_REL`(사원기술 연결) 테이블 추가** — §8 명시 항목(1~11번)이 모두 완료되어, §3/§4 로드맵상 가장 앞선 미완료 Phase(Phase 2, 60%)의 다음 순서(ERD §3.6, `HR_EMPL_SKILL_REL`)로 이어서 진행. `backend/app/models/hr_empl_skill_rel.py` 신규 작성(`HR_EMPL_MST`/`HR_SKILL_MST` FK, `PRFCY_LEVL` CHECK 1~5 — 컬럼명 큰따옴표 처리 포함, ERD상 `PRFCY_LEVL`에 NOT NULL 표기가 없어 nullable로 구현), `app/models/__init__.py`에 등록. Alembic 리비전 `backend/alembic/versions/ea8f648e460f_create_hr_empl_skill_rel_table.py`를 이전 리비전(`83fc676b952e`) 뒤에 체이닝해 수기 작성. Phase 2 진행률 60%→65%로 갱신(16개 테이블 중 11개 모델+마이그레이션 작성 완료, 10개 실 DB 검증). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경에 `alembic`/`sqlalchemy` 미설치로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- **Phase 2 계속 — `HR_EMPL_ROLE_REL`(사원역할 연결) 테이블 추가** — ERD §3.6-1 순서에 따라 이어서 진행. `backend/app/models/hr_empl_role_rel.py` 신규 작성(`HR_EMPL_MST`/`HR_JIKMU_MST` FK, `(EMPL_ID, JIKMU_ID)` 복합 UNIQUE 제약, `IS_PRIMARY` 불리언). `IS_PRIMARY=TRUE` 행의 `JIKMU_ID`가 `HR_EMPL_MST.JIKMU_ID`와 일치해야 하는 규칙은 설계서 §5.5에 따라 DB 제약이 아닌 애플리케이션 레이어 검증 대상임을 모델 주석에 명시(Phase 3에서 구현). `app/models/__init__.py`에 등록. Alembic 리비전 `backend/alembic/versions/ca8a45d7771f_create_hr_empl_role_rel_table.py`를 이전 리비전(`ea8f648e460f`) 뒤에 체이닝해 수기 작성. Phase 2 진행률 65%→70%로 갱신(16개 테이블 중 12개 모델+마이그레이션 작성 완료, 10개 실 DB 검증). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- **§8 다음 작업 개편 및 `HR_AVAIL_SNAP`(가동가능 스냅샷) 테이블 추가** — §8 섹션을 Phase 2 잔여 작업 중심의 새 큐(0~10번)로 개편(항목 0·1은 이미 완료되어 있어 근거와 함께 완료 처리). ERD §3.7 순서에 따라 `backend/app/models/hr_avail_snap.py` 신규 작성 — `REG_DTTM`만 있고 `UPD_DTTM`이 없는 append-only 스냅샷 구조라 `SysAuditLog`와 동일하게 별도 Mixin 없이 직접 선언, `AVAIL_STAT_CD` CHECK 제약(컬럼명 큰따옴표 처리 포함) 추가. `AVAIL_STRT_DT` 산정 로직(`backend/docs/AVAILABILITY_CALC_SPEC.md`)의 실제 계산 배치 구현은 Phase 7 몫으로 모델 주석에 명시 — 이 리비전은 스키마만 다룸. `app/models/__init__.py`에 등록. Alembic 리비전 `backend/alembic/versions/611b8a04d673_create_hr_avail_snap_table.py`를 이전 리비전(`ca8a45d7771f`) 뒤에 체이닝해 수기 작성. Phase 2 진행률 70%→75%로 갱신(16개 테이블 중 13개 모델+마이그레이션 작성 완료, 10개 실 DB 검증). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- **§8 다음 작업을 Rolling Backlog로 재설정 및 `PJT_RSRC_REQ`(리소스 요청) 테이블 추가** — §8 헤더를 "누적 완료 목록이 아닌 다음 작업 큐" 원칙으로 재정의, 완료된 `HR_EMPL_ROLE_REL`/`HR_AVAIL_SNAP` 항목을 큐에서 제거하고 §7/§11 근거만 남김(Phase 1 마무리 항목은 0번 번호를 유지하되 완료 표시로 정정). 이어서 ERD §3.10 순서에 따라 `backend/app/models/pjt_rsrc_req.py` 신규 작성(`PJT_MST`/`SYS_USER_MST`/`HR_JIKMU_MST`(nullable) FK, `REQ_SKILL_JSON` JSONB, `REQ_STAT_CD` CHECK 제약). `app/models/__init__.py`에 등록. Alembic 리비전 `backend/alembic/versions/afbd73237178_create_pjt_rsrc_req_table.py`를 이전 리비전(`611b8a04d673`) 뒤에 체이닝해 수기 작성. Phase 2 진행률 75%→80%로 갱신(16개 테이블 중 14개 모델+마이그레이션 작성 완료, 10개 실 DB 검증). §8 큐를 다시 갱신해 완료 항목 제거 및 나머지 항목 재번호(1~6). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- **`PJT_RCMD_RSLT`(추천 결과) 테이블 추가** — ERD §3.11 순서에 따라 이어서 진행. `backend/app/models/pjt_rcmd_rslt.py` 신규 작성 — `REG_DTTM`만 있고 `UPD_DTTM`이 없는 append-only 구조라 `SysAuditLog`/`HrAvailSnap`과 동일하게 별도 Mixin 없이 직접 선언, `PJT_RSRC_REQ`/`HR_EMPL_MST` FK, `SCORE_DTL_JSON`(JSONB) 포함. 추천 점수 산정 가중치 실제 계산 로직은 Phase 5 구현 몫으로 모델 주석에 명시 — 이 리비전은 스키마만 다룸. `app/models/__init__.py`에 등록. Alembic 리비전 `backend/alembic/versions/1a7979587160_create_pjt_rcmd_rslt_table.py`를 이전 리비전(`afbd73237178`) 뒤에 체이닝해 수기 작성. Phase 2 진행률 80%→85%로 갱신(16개 테이블 중 15개 모델+마이그레이션 작성 완료, 10개 실 DB 검증). §8 큐에서 완료 항목 제거 및 나머지 재번호(1~5). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인 (아래 검증 결과 참조)
- **`SYS_BATCH_HIS`(배치 실행 이력) 테이블 추가 — ERD 16개 테이블 모델·마이그레이션 전체 작성 완료** — ERD §3.15 순서에 따라 마지막 테이블 작업. `backend/app/models/sys_batch_his.py` 신규 작성 — ERD상 이 테이블만 유일하게 NOT NULL 등 제약 표기가 전혀 없어 `BATCH_ID`(PK)를 제외한 전 컬럼을 nullable로 반영, FK 없는 독립 테이블, `REG_DTTM`만 있어 다른 Mixin 없이 직접 선언. `app/models/__init__.py`에 등록. Alembic 리비전 `backend/alembic/versions/a5754b3eb5f3_create_sys_batch_his_table.py`를 이전 리비전(`1a7979587160`) 뒤에 체이닝해 수기 작성 — 이로써 `28ce52377e32`(최초)부터 `a5754b3eb5f3`(현재 head)까지 8개 리비전이 분기 없는 단일 선형 체인으로 연결됨을 `revision`/`down_revision` 전수 대조로 확인(§8 "전체 Alembic 마이그레이션 체인 점검" 항목 겸 완료 처리). Phase 2 진행률 85%→90%로 갱신(16개 테이블 전체 모델+마이그레이션 작성 완료, 이 중 10개만 실 DB 검증). §8 큐를 Seed 작성/실 서버 적용 검증/Phase 2 완료 기준 점검 3개 항목으로 재정리(1~3). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — 모델-마이그레이션 컬럼 일치 여부는 정적 비교로 확인, 리비전 체인 연결은 8개 파일 전수 대조로 확인 (아래 검증 결과 참조)
- **`HR_JIKGUP_MST`(10종)/`HR_JIKMU_MST`(12종) Seed 데이터 작성** — 설계서 §5.3.2/§5.3.3에 확정 값으로 명시되어 있어(로드맵 §9 리스크 대상 아님) `backend/app/db/seed/hr_jikgup_mst_seed.py`, `hr_jikmu_mst_seed.py` 신규 작성(기존 `hr_skill_mst_seed.py`/`sys_role_mst_seed.py`와 동일한 파일 위치·스타일 재사용). 두 테이블은 이전 리비전(`28ce52377e32`)에서 이미 생성·적용된 상태라 그 리비전을 되돌려 수정하지 않고, 새 Alembic 리비전 `backend/alembic/versions/370c95546556_seed_hr_jikgup_mst_and_hr_jikmu_mst.py`를 현재 head(`a5754b3eb5f3`) 뒤에 체이닝해 `op.bulk_insert`로 Seed만 추가(`SYS_ROLE_MST` Seed 반영 때와 동일한 패턴). 이로써 로드맵 §11 "Seed 데이터 입력(`SYS_ROLE_MST`+`HR_JIKGUP_MST`+`HR_JIKMU_MST`)" 항목이 3종 모두 완료됨. Phase 2 진행률 90%→95%로 갱신. §8 큐에서 완료 항목 제거 및 나머지 재번호(1~2). **실 DB 연결 기반 `alembic upgrade head` 적용 검증은 로컬 환경 제약으로 미실시** — Seed 데이터 건수(10건/12건) 및 필드 구조는 정적 검증으로 확인 (아래 검증 결과 참조)
- **Phase 2 완료 — 실 서버 최종 검증 (`alembic upgrade head`, 16개 테이블, Seed, 백업)** — 사용자 확인 하에 `sudo docker compose`로 실 서버에 직접 접근해 이번 세션에서 미실행 상태로 남아있던 검증을 전부 수행: `docker compose up -d --build api worker`로 최신 코드 반영 후 `alembic upgrade head` 실행, `83fc676b952e`→`370c95546556`(현재 head)까지 대기 중이던 7개 리비전 전부 정상 적용 확인. `\dt` 결과 ERD 16개 테이블 + `alembic_version` 총 17개 relation 확인, `SELECT COUNT(*)`로 `SYS_ROLE_MST`(6)/`HR_JIKGUP_MST`(10)/`HR_JIKMU_MST`(12) Seed 정상 삽입 확인, `curl /health`·`curl /api/v1/employees` 정상 응답 확인. 이전까지 "실 DB 미검증"으로 남아있던 6개 테이블(`HR_EMPL_SKILL_REL`/`HR_EMPL_ROLE_REL`/`HR_AVAIL_SNAP`/`PJT_RSRC_REQ`/`PJT_RCMD_RSLT`/`SYS_BATCH_HIS`)과 Seed 3종을 전부 "실 서버 DB 적용 검증 완료"로 갱신(§4/§11). 추가로 `backup/backup_db.sh`를 실 서버에서 수동 실행해 `pg_dump` 백업 파일(`hrm_20260703_132344.sql.gz`, `CREATE TABLE` 17건 포함) 정상 생성을 확인 — Phase 2 "완료 기준" 3개 항목(테이블 생성/Seed 입력/백업 파일 생성)이 전부 충족되어 **Phase 2를 100% 완료로 전환**. crontab 자동 등록(매일 02:00)은 별도 배치 운영 항목(`SYS_DB_BACKUP`, Phase 7)으로 이미 분리되어 있어 Phase 2 완료 판정에 영향 없음. §8 큐를 Phase 3 잔여 작업(Pydantic 스키마·API 구현·인증·감사 로그 등 11개 항목) 중심으로 전면 재구성. 참고: `worker` 컨테이너는 Phase 7까지 placeholder라 실행 후 종료→재시작을 반복하는 것이 의도된 정상 상태임을 로그로 확인(`docker compose logs worker`)
- **Pydantic v2 스키마 작성 — 16개 테이블 전체 조회(Out) 스키마 완료 (§8 다음 작업 1번)** — 사용자가 현재 `novauser` 계정도 `docker` 그룹 권한을 갖고 있음을 알려주어(`sg docker -c "..."`로 그룹 즉시 적용 확인), 이후 `sudo` 없이 직접 실 서버 컨테이너에 접근해 작업. 기존 `EmployeeOut`(1개) 외 나머지 15개 테이블 도메인에 대해 `backend/app/schemas/`에 조회 전용 스키마 신규 작성 — `hr_dept_mst.py`(`DepartmentOut`), `hr_jikgup_mst.py`(`PositionOut`), `hr_jikmu_mst.py`(`JobTypeOut`), `hr_skill_mst.py`(`SkillOut`), `hr_empl_skill_rel.py`(`EmployeeSkillOut`), `hr_empl_role_rel.py`(`EmployeeRoleOut`), `hr_avail_snap.py`(`AvailabilitySnapshotOut`), `pjt_mst.py`(`ProjectOut`), `pjt_asgn_his.py`(`AssignmentOut`), `pjt_rsrc_req.py`(`ResourceRequestOut`), `pjt_rcmd_rslt.py`(`RecommendationResultOut`), `sys_user_mst.py`(`SysUserOut` — `ENCR_PWD`는 설계서 §11 보안 원칙에 따라 스키마에서 의도적으로 제외), `sys_role_mst.py`(`RoleOut`), `sys_audit_log.py`(`AuditLogOut`), `sys_batch_his.py`(`BatchHistoryOut`). 각 모델의 Mixin 종류(`TimestampMixin`/`AuditMixin`/단독 `REG_DTTM`)를 정확히 반영해 필드 구성. **검증을 이례적으로 강하게 수행**: `docker compose up -d --build api`로 이미지 재빌드 후, 컨테이너 내부에서 실제 `python3 -c "import ..."`로 15개 스키마 전부 정상 임포트 확인, `HR_JIKGUP_MST`/`SYS_ROLE_MST` 실 데이터 행을 SQLAlchemy로 조회해 `PositionOut`/`RoleOut`으로 `model_validate()` 변환까지 성공 확인(`RoleOut`에서 `PERM_JSON` JSONB 필드와 `REG_DTTM`의 KST 타임존 정상 역직렬화 확인). `ENCR_PWD`가 `SysUserOut.model_fields`에 없음을 코드로 재확인. Phase 3 진행률 20%→28%로 갱신(FastAPI 구조/`/health`/CORS/SQLAlchemy 모델/Pydantic 스키마 5개 항목 완료). §8 큐에서 완료 항목 제거 및 나머지 재번호(1~9)
- **부서/직급/직무 코드 조회 API 구현 (§8 다음 작업 1번)** — `backend/app/repositories/codes.py`(신규, `HR_DEPT_MST`/`HR_JIKGUP_MST`/`HR_JIKMU_MST` 세 코드 마스터가 소규모라 백로그 항목과 동일하게 한 모듈로 묶어 구현) 및 `backend/app/api/v1/codes.py`(신규, `GET /api/v1/departments`·`/positions`·`/job-types`, 각 정렬 컬럼(`DEPT_ORD`/`JIKGUP_ORD`/`SORT_ORD`) 기준 정렬 + `use_yn` 필터)를 `employees.py`/`hr_empl_mst.py`와 동일한 리포지토리+라우터 패턴으로 작성. `backend/app/api/v1/router.py`에 등록. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: `docker compose up -d --build api` 재빌드 후 `curl /api/v1/departments`(0건, `HR_DEPT_MST` Seed 없어 정상)·`/positions`(10건)·`/job-types`(12건) 정상 응답 확인, `openapi.json`에서 3개 경로 전부 등록 확인. Phase 3 진행률 28%→33%로 갱신, §11 "부서/직급 코드 API" 완료 체크(범위상 조회만 구현이라 "직무 유형 CRUD API" 항목은 조회만 완료로 별도 표기, 등록/수정 미구현 유지). §8 큐에서 완료 항목 제거 및 재번호(1~9)
- **기술 CRUD API 구현 (§8 다음 작업 1번)** — `employees.py` 패턴을 그대로 재사용해 조회/등록/수정(GET/POST/PATCH) 구현. `backend/app/schemas/hr_skill_mst.py`에 `SkillCreate`/`SkillUpdate` 추가, `backend/app/schemas/hr_empl_skill_rel.py`에 `EmployeeSkillCreate`/`EmployeeSkillUpdate` 추가(`PRFCY_LEVL`은 ERD CHECK 제약(1~5)과 동일하게 `Field(ge=1, le=5)`로 검증). `backend/app/repositories/hr_skill_mst.py`(신규, `list_skills`/`get_skill`/`create_skill`/`update_skill`, `skill_grp_cd`/`use_yn` 필터), `backend/app/repositories/hr_empl_skill_rel.py`(신규, `list_employee_skills`/`get_employee_skill`/`create_employee_skill`/`update_employee_skill`, `empl_id`/`skill_id` 필터) 작성. 라우터 `backend/app/api/v1/skills.py`(`GET`/`POST /api/v1/skills`, `PATCH /api/v1/skills/{skill_id}`), `backend/app/api/v1/employee_skills.py`(`GET`/`POST /api/v1/employee-skills`, `PATCH /api/v1/employee-skills/{empl_skill_id}`) 신규 작성, `backend/app/api/v1/router.py`에 등록. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: `docker compose up -d --build api` 재빌드 후 `POST /api/v1/skills`(정상 생성 확인), `GET /api/v1/skills`(`use_yn` 기본 필터 동작 확인), `PATCH /api/v1/skills/{id}`(부분 업데이트 확인), `POST /api/v1/employee-skills`에 `PRFCY_LEVL=9`(범위 밖) 전달 시 422, 존재하지 않는 `EMPL_ID`로 전달 시 409(FK 위반→`IntegrityError` 변환) 정상 확인. 현재 `HR_EMPL_MST`에 실 데이터가 없어 정상 케이스(유효 FK)의 등록/조회까지는 검증하지 못함 — 검증 결과 참조. Phase 3 진행률 33%→39%로 갱신. §8 큐에서 완료 항목 제거 및 재번호(1~8)
- **프로젝트 CRUD API 구현 (§8 다음 작업 1번)** — `employees.py`/`hr_empl_mst.py` 패턴(skip/limit 페이지네이션 + total 응답)을 재사용해 조회/등록/수정(GET/POST/PATCH) 구현. `backend/app/schemas/pjt_mst.py`에 `ProjectCreate`/`ProjectUpdate`(`PJT_STAT_CD`는 모델의 `PJT_STAT_CODES` 상수를 `Literal` 타입으로 재사용해 DB CHECK 제약과 값 목록 어긋남 방지) 및 `ProjectListResponse` 추가. `backend/app/repositories/pjt_mst.py`(신규, `list_projects`/`get_project`/`create_project`/`update_project`, `pjt_stat_cd` 필터 + skip/limit) 작성. 라우터 `backend/app/api/v1/projects.py`(신규, `GET`/`POST /api/v1/projects`, `PATCH /api/v1/projects/{pjt_id}`) 작성, `backend/app/api/v1/router.py`에 등록. `PJT_CD` UNIQUE 위반은 `IntegrityError`를 잡아 409로 변환. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: `docker compose up -d --build api` 재빌드 후 `POST /api/v1/projects`(정상 생성 확인), 동일 `PJT_CD` 재등록 시 409, `PATCH`에 잘못된 `PJT_STAT_CD`("BOGUS") 전달 시 422, 유효한 상태값으로 `PATCH` 후 `GET ?pjt_stat_cd=` 필터 정상 동작, 존재하지 않는 `pjt_id`로 `PATCH` 시 404 전부 확인. Phase 3 진행률 39%→44%로 갱신. §8 큐에서 완료 항목 제거 및 재번호(1~7)
- **투입 관리 API 구현 (§8 다음 작업 1번)** — `employees.py`/`projects.py` 패턴을 재사용해 조회/등록/수정(GET/POST/PATCH) 구현. `backend/app/schemas/pjt_asgn_his.py`에 `AssignmentCreate`/`AssignmentUpdate`/`AssignmentListResponse` 추가(`ASGN_TYPE_CD`/`ASGN_STAT_CD`는 모델 상수 기반 `Literal`, `ALLOC_RT`는 `Field(ge=0, le=100)`로 CHECK 제약과 동일하게 검증). `backend/app/repositories/pjt_asgn_his.py`(신규, `list_assignments`/`get_assignment`/`create_assignment`/`update_assignment` 외 `sum_overlapping_alloc_rt` 신규 — 동일 사원·겹치는 기간의 유효(`PLANNED`/`ACTIVE`) 투입 건 ALLOC_RT 합계 계산) 작성. 모델 주석(ERD §3.9/설계서 §5.5)에 명시된 "동일 사원 동일 기간 ALLOC_RT 합계 100% 초과 금지" 정합성 규칙을 라우터(`backend/app/api/v1/assignments.py`, 신규)의 등록/수정 시점에 적용해 초과 시 409로 거부 — 이 규칙의 집계 대상 상태(`PLANNED`/`ACTIVE`만 포함, `CANCELED`/`DONE` 제외)는 설계서에 명문화되어 있지 않은 MVP 해석이라 코드 주석에 근거와 함께 명시(§9 리스크 참고). `backend/app/api/v1/router.py`에 등록. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: `docker compose up -d --build api` 재빌드 후, 테스트용 부서·사원·프로젝트 데이터를 임시 생성해 동일 사원·동일 기간에 ALLOC_RT 60%+40%=100% 등록 성공, 60%+50%(=110%) 등록 시 409, 기존 60%건을 70%로 수정 시(40%와 합 110%) 409, 상태를 `CANCELED`로 변경 시 집계 제외되어 정상 처리, 존재하지 않는 `asgn_id`로 `PATCH` 시 404 전부 확인. 검증에 사용한 임시 부서/사원/프로젝트/투입이력 데이터는 검증 직후 모두 삭제해 DB에 남기지 않음. Phase 3 진행률 44%→50%로 갱신. §8 큐에서 완료 항목 제거 및 재번호(1~6)
- **JWT 인증 API 구현 (§8 다음 작업 1번)** — 로그인/토큰 갱신/로그아웃 3개 엔드포인트 신규 구현. `backend/app/core/security.py`(신규, `passlib`(bcrypt) 비밀번호 해싱, `python-jose` JWT 인코딩/디코딩, 액세스(60분)/리프레시(7일) 토큰 발급 — 만료 시간은 기존 `Settings.ACCESS_TOKEN_EXPIRE_MINUTES`/`REFRESH_TOKEN_EXPIRE_DAYS`(이미 `.env.example`/`config.py`에 존재) 재사용), `backend/app/schemas/auth.py`(신규, `LoginRequest`/`TokenResponse`/`RefreshRequest`/`AccessTokenResponse`), `backend/app/repositories/sys_user_mst.py`(신규, `get_user_by_login_id`/`get_user`/`update_last_login`), `backend/app/api/v1/auth.py`(신규, `POST /api/v1/auth/{login,refresh,logout}`) 작성. `backend/app/api/v1/router.py`에 등록. 로그인은 계정 미존재/비밀번호 불일치/비활성/비밀번호 미설정을 모두 동일한 401로 처리(계정 존재 여부 비노출), 로그아웃은 stateless JWT 특성상 서버 측 즉시 무효화 저장소가 아직 없어 클라이언트 토큰 폐기로 처리(§9 리스크로 기록, RBAC 미들웨어 도입 시 Redis 블랙리스트 검토 예정). **실 서버 컨테이너 재빌드 중 `passlib[bcrypt]==1.7.4`가 최신 `bcrypt`(5.0.0) 설치로 인해 비밀번호 해싱 시 `AttributeError`/`ValueError`를 던지는 상위 호환성 버그를 발견** — `backend/requirements.txt`에 `bcrypt==4.0.1` 고정 추가로 해결(§9 리스크 기록). 재빌드 후 검증용 임시 역할·사용자 데이터로 로그인 성공(토큰 발급, `LAST_LGN_DTTM` 갱신 확인), 비밀번호 오류 401, 존재하지 않는 사용자 401, 리프레시 토큰으로 액세스 토큰 재발급, 액세스 토큰을 리프레시 토큰으로 오용 시 401(토큰 타입 검증), 위조 토큰 401, 로그아웃 204 전부 확인 후 테스트 데이터 삭제. `.env`의 `JWT_SECRET_KEY`는 이미 설정되어 있음을 확인했으며 직접 수정하지 않음. Phase 3 진행률 50%→56%로 갱신. §8 큐에서 완료 항목 제거 및 재번호(1~5)
- **RBAC 권한 미들웨어 구현 — 부분 완료 (§8 다음 작업 1번, 진행 중 유지)** — `backend/app/api/deps.py`(신규) 작성: `get_current_user`(액세스 토큰 검증 + 활성 사용자 조회, `Authorization: Bearer` 헤더 필수), `require_permission(screen, action)`(역할별 `SYS_ROLE_MST.PERM_JSON`의 화면×버튼 권한 검사, 미권한 시 403) 의존성 제공. `PERM_JSON`에 이미 정의된 화면 키(`employees`/`skills`/`projects`/`assignments`)와 정확히 매칭되는 5개 라우터(`employees.py`, `skills.py`, `employee_skills.py`(→`skills` 화면 재사용, 사원기술 연결은 기술 관리 화면의 일부 기능으로 취급), `projects.py`, `assignments.py`)의 조회/등록/수정 엔드포인트에 `dependencies=[Depends(require_permission(...))]`로 적용. `codes.py`(부서/직급/직무 유형)는 `PERM_JSON`에 `job_types` 화면 키만 있고 `departments`/`positions`는 정의되어 있지 않아 임의 추정 대신 이번 적용 범위에서 제외(§9 리스크 기록) — 이 때문에 백로그 항목은 "완료"가 아닌 "진행 중"으로 유지. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 인증 토큰 없이 `GET /employees`/`POST /projects` 호출 시 401, 위조 토큰 401, VIEWER 역할 토큰으로 `GET /employees`(권한 있음) 200·`POST /employees`(권한 없음) 403·`GET /skills`(권한 없음) 403, PM 역할 토큰으로 `GET/POST /projects`(권한 있음) 200/201·`POST /skills`(권한 없음) 403 — `PERMISSION_MATRIX.md`/Seed에 정의된 역할별 권한표와 정확히 일치함을 확인. 검증에 사용한 임시 사용자/프로젝트 데이터는 검증 직후 삭제. Phase 3 진행률은 부분 완료라 56%로 유지(보수적 갱신 원칙)
- **`SYS_AUDIT_LOG` 감사 로그 미들웨어 구현 (§8 다음 작업 2번)** — 진짜 ASGI 미들웨어 대신 RBAC 구현(§8 1번)과 동일하게 라우터별 명시적 호출 방식으로 구현(도메인마다 BFR/AFT 스냅샷 구조가 달라 범용 ASGI 미들웨어로는 표현이 어려움). `backend/app/repositories/sys_audit_log.py`(신규, `create_audit_log`), `backend/app/core/audit.py`(신규, `record_audit` — 요청의 클라이언트 IP/User-Agent를 자동 포함해 `SYS_AUDIT_LOG`에 기록) 작성. `employees.py`/`skills.py`/`employee_skills.py`/`projects.py`/`assignments.py`의 등록(CREATE)·수정(UPDATE) 엔드포인트에 적용 — 수정 시에는 갱신 전 상태를 각 도메인의 Out 스키마로 스냅샷해 `BFR_VAL_JSON`에, 갱신 후 상태를 `AFT_VAL_JSON`에 기록. `auth.py` 로그인 성공 시에도 `ACT_CD='LOGIN'` 기록 추가(실패한 로그인은 `SYS_AUDIT_LOG.USER_ID`가 NOT NULL FK라 행위자를 특정할 수 없어 기록하지 않음, 사유 주석 명시). RBAC 적용 라우터에서 이미 `require_permission`으로 확보한 `current_user`를 재사용하도록 각 라우터의 `dependencies=[...]` 방식을 `current_user: SysUserMst = Depends(...)` 파라미터 방식으로 일부 변경(권한 검사 로직 자체는 변경 없음). `codes.py`(부서/직급/직무 유형)는 RBAC 미적용 상태와 동일하게 이번 범위에서 제외. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 테스트용 ADMIN 역할 사용자로 로그인 → `POST /api/v1/skills`(등록) → `PATCH /api/v1/skills/{id}`(수정) 실행 후 `SYS_AUDIT_LOG`를 직접 조회해 `LOGIN`/`CREATE`/`UPDATE` 3건이 올바른 `USER_ID`/`TGT_TBL_NM`/`TGT_ID`/`CLNT_IP`/`USER_AGT`로 기록되고, `UPDATE` 건의 `BFR_VAL_JSON`/`AFT_VAL_JSON`이 실제 변경 전후 값(`USE_YN: true→false`)과 일치함을 확인. 검증에 사용한 임시 사용자/기술/감사로그 데이터는 검증 직후 삭제. Phase 3 진행률 56%→61%로 갱신. §8 큐에서 완료 항목 제거 및 재번호(1~4)
- **RBAC 권한 미들웨어 — `codes` 화면 권한 신설로 잔여 범위 완료 (§9 리스크 해소)** — 운영팀 확인 결과(2026-07-03), 부서(`departments`)/직급(`positions`)은 MVP에서 독립 화면으로 보지 않고 "공통 코드/기준정보"로 취급하기로 확정. 별도 화면 키를 만들지 않고 `SYS_ROLE_MST.PERM_JSON`에 공통 `codes` 키를 신설 — `codes.view`는 6개 역할 전체 허용, `codes.create`/`update`/`delete`는 ADMIN/HR_MGR만 허용. `backend/app/db/seed/sys_role_mst_seed.py`의 6개 역할 `PERM_JSON`에 `codes` 반영(신규 Seed 소스 기준) 및 Alembic 리비전 `9c1f3a5d2b7e_add_codes_perm_to_sys_role_mst.py`를 이전 head(`370c95546556`) 뒤에 체이닝해 작성 — `SYS_ROLE_MST`는 이미 실 DB에 Seed 적용된 상태라 해당 리비전을 되돌려 수정하지 않고 `jsonb_set`으로 기존 행을 갱신(다운그레이드는 `#-` 연산자로 `codes` 키 제거). `GET /api/v1/job-types` 조회도 직무 유형 관리 화면의 등록/수정/삭제 권한(`job_types.*`, A H 전용)과 별개로 `codes.view` 정책을 함께 적용해 전 역할이 조회 가능하도록 함. `backend/app/api/v1/codes.py`의 `GET /departments`·`/positions`·`/job-types` 3개 엔드포인트에 `require_permission("codes", "view")` 적용 — 이로써 인증 없이 호출 가능하던 마지막 업무 API가 제거됨(`/health`, `/auth/login`·`/refresh`·`/logout`만 명시적 공개 API로 유지). `backend/docs/PERMISSION_MATRIX.md`에 `codes` 권한 섹션(화면 목록 표에는 미포함, 별도 설명과 역할×버튼 매트릭스 추가) 및 §4 `screen_key` 목록 갱신(13종→14종). **실 서버에서 실제 검증**: `alembic upgrade head`로 리비전 적용 후 `SELECT`로 6개 역할의 `PERM_JSON->'screens'->'codes'` 값이 스펙대로(ADMIN/HR_MGR 전권, 나머지 4개 역할 view만) 반영됨을 확인. 인증 없이 `GET /departments`/`/positions`/`/job-types` 호출 시 전부 401로 전환됨을 확인, VIEWER 역할 테스트 사용자로 로그인 후 3개 엔드포인트 전부 200 정상 응답 확인. 검증에 사용한 임시 사용자 데이터는 검증 직후 삭제. Phase 3 진행률 61%→67%로 갱신(RBAC 항목이 "진행 중"에서 "완료"로 전환됨에 따라 완료 항목 수 반영), §11 "RBAC 권한 미들웨어 구현" 완료 체크로 정정, §9 리스크 "departments/positions/job-types 화면 권한 키 미정" "주의→해소" 처리
- **사원 퇴직 처리 API 구현 (§8 다음 작업 1번)** — `backend/app/repositories/hr_empl_mst.py`에 `retire_employee`(신규) 추가 — 로우 삭제가 아니라 `EMPL_STAT_CD='RETIRED'` 전환 + `RETIR_DT` 기록(미지정 시 오늘 날짜)만 수행하는 소프트 삭제로 구현(ERD/설계서 원칙상 사원 이력을 물리적으로 삭제하지 않음). `backend/app/api/v1/employees.py`에 `DELETE /api/v1/employees/{empl_id}` 라우터 추가 — `retir_dt` 쿼리 파라미터로 퇴직일 수동 지정 가능, 이미 퇴직 처리된 사원이면 409, 미존재 시 404, 기존 `employees` 라우터와 동일하게 `require_permission("employees", "delete")`(ADMIN/HR_MGR만 허용, PERM_JSON 기존 값 그대로 재사용) 및 `record_audit`(`ACT_CD='DELETE'`, 변경 전/후 스냅샷)를 적용. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 테스트용 부서·ADMIN 사용자·사원 데이터를 임시 생성해 `DELETE`로 `EMPL_STAT_CD`가 `ACTIVE→RETIRED`, `RETIR_DT`가 오늘 날짜로 정상 전환됨을 확인, 동일 사원 재차 `DELETE` 시 409, 존재하지 않는 `empl_id`에 404, 인증 없이 호출 시 401, `delete` 권한이 없는 VIEWER 역할 토큰으로 호출 시 403 전부 확인. `SYS_AUDIT_LOG`에 `ACT_CD='DELETE'` 건이 `BFR_VAL_JSON.EMPL_STAT_CD='ACTIVE'`/`AFT_VAL_JSON.EMPL_STAT_CD='RETIRED'`로 정확히 기록됨을 `psql`로 직접 확인. 검증에 사용한 임시 데이터는 검증 직후 전부 삭제. Phase 3 진행률 67%→72%로 갱신(사원 CRUD API가 "진행 중"에서 "완료"로 전환), §11 "사원 CRUD API" 완료 체크로 정정, §8 큐에서 완료 항목 제거 및 재번호(1~2)
- **페이지네이션 공통 처리 구현 (§8 다음 작업 1번)** — `backend/app/core/pagination.py`(신규, `PaginationParams` — FastAPI "classes as dependencies" 패턴으로 `skip`/`limit` Query 파라미터를 하나로 추출), `backend/app/schemas/pagination.py`(신규, `PaginatedResponse[T]` Pydantic 제네릭 — `total`/`skip`/`limit`/`items` 구조 재사용) 작성. 기존 `EmployeeListResponse`/`ProjectListResponse`/`AssignmentListResponse`가 각자 동일 구조를 중복 정의하던 것을 `PaginatedResponse[EmployeeOut]` 등 타입 별칭으로 대체(응답 JSON 형태는 기존과 동일하게 유지). `employees.py`/`projects.py`/`assignments.py`의 목록 조회 라우터에서 개별 `Query(0, ge=0)`/`Query(20, ge=1, le=200)` 선언을 `pagination: PaginationParams = Depends()`로 교체. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 3개 엔드포인트 모두 기본값(`skip=0, limit=20`) 및 커스텀 값(`skip=5&limit=10`) 정상 응답, `limit=0`/`limit=300`(범위 밖) 시 422 검증 그대로 유지됨을 확인 — 응답 JSON 키(`total`/`skip`/`limit`/`items`) 변경 없음. 단, `/openapi.json`의 스키마명이 `EmployeeListResponse` 등에서 `PaginatedResponse_EmployeeOut_` 형태로 바뀌는 부수 효과 발견해 §9 리스크로 기록(응답 바디 자체는 무영향, 프론트엔드는 현재 목데이터 기반이라 당장 영향 없음). Phase 3 진행률 72%→78%로 갱신, §11 "페이지네이션 공통 처리 구현" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1)
- **OpenAPI 문서(`/docs`) 확인 (§8 다음 작업 1번)** — 코드 변경 없이 실 서버에서 실제 검증만 수행. `curl`로 `/docs`(Swagger UI), `/redoc`, `/openapi.json` 전부 200 정상 응답 확인. `/openapi.json` 파싱 결과 현재까지 구현된 22개 엔드포인트(auth 3개, employees 4개, skills 3개, employee-skills 3개, projects 3개, assignments 3개, codes 3개)가 각자 올바른 태그·설명(각 함수 docstring이 `description`으로 자동 반영됨)·응답 코드로 노출됨을 확인. `HTTPBearer` 보안 스키마가 `components.securitySchemes`에 자동 등록되어 있고, 인증이 필요한 엔드포인트(예: `GET /employees`)에는 `security: [{"HTTPBearer": []}]`가, 공개 엔드포인트(`POST /auth/login`)에는 `security` 필드가 없음을 확인 — RBAC 적용 범위가 OpenAPI 스펙에도 정확히 반영되어 있음을 재확인. Phase 3 진행률 78%→83%로 갱신, §11 "OpenAPI 문서 확인" 완료 체크, §8 큐가 비어 §4 Phase 3 "주요 작업" 표에서 아직 미착수인 3개 항목(가동률 계산 API, 대시보드 집계 API, Excel Import/Export API)으로 새 큐 구성
- **가동률 계산 API 구현 (§8 다음 작업 1번)** — `backend/app/repositories/hr_avail_snap.py`(신규, `compute_availability`)에 `AVAILABILITY_CALC_SPEC.md` §2/§4 로직을 그대로 구현: 기준일 현재 `ASGN_STAT_CD='ACTIVE'`이고 투입 기간 내이며 `ASGN_TYPE_CD IN ('RUNNING','COMMITTED')`인 `PJT_ASGN_HIS` 행만 집계해 `TOT_ALLOC_RT` 산출, 0%=`AVAILABLE`/1~99%=`PARTIAL`/≥100%=`FULL`(`MAX(ASGN_END_DT)+1일`, 종료일 NULL 존재 시 `AVAIL_STRT_DT=None`+`DATA_QUALITY_WARNING=True`) 3단계 산정. `backend/app/schemas/hr_avail_snap.py`에 `AvailabilityCalcOut` 추가. `backend/app/api/v1/availability.py`(신규) `GET /api/v1/availability/{empl_id}`(`snap_dt` 쿼리 파라미터로 기준일 지정 가능, 기본 오늘) 작성, `require_permission("availability", "view")` 적용(기존 PERM_JSON `availability.view` 값 그대로 재사용), `router.py`에 등록. **중요한 설계 결정**: 이 API는 `HR_AVAIL_SNAP` 테이블에 스냅샷 행을 저장하지 않는 순수 즉시 계산(read-only) 엔드포인트로 구현 — 스냅샷 생성·자동 배치(`HR_AVAIL_SNAP_GEN`, 매일 01:00)는 모델 주석과 스펙 문서에 이미 Phase 7 몫으로 명시되어 있어 중복 구현하지 않기 위함(§9 참고 사항 없이 스펙 문서 원칙을 그대로 따른 것이라 별도 리스크로 기록하지 않음). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 테스트용 부서·사원 5명·프로젝트·투입 데이터를 임시 생성해 5가지 케이스 전부 스펙과 정확히 일치함을 확인 — ① 투입 없음→`AVAILABLE`(기준일), ② 60% 투입→`PARTIAL`(기준일), ③ 100% 투입(종료일 있음)→`FULL`(`종료일+1일`), ④ 100% 투입(종료일 NULL)→`FULL`+`AVAIL_STRT_DT=null`+`DATA_QUALITY_WARNING=true`, ⑤ `ASGN_TYPE_CD='PROPOSED'`+`ASGN_STAT_CD='PLANNED'` 80% 투입→집계 제외되어 `AVAILABLE`. 존재하지 않는 사원 404, 무인증 401도 확인. 검증에 사용한 임시 데이터는 검증 직후 전부 삭제. Phase 3 진행률 83%→89%로 갱신, §5 "가동 가능일 자동 계산" 항목을 "예정→진행 중"(즉시 계산 API는 완료, 자동 배치는 Phase 7 미구현)으로 갱신, §11 "가동률 계산 API" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1~2)
- **대시보드 집계 API 구현 (§8 다음 작업 1번)** — `[DESIGN]HRM_Screen_Design.md` SCR-002(대시보드) "연동 API" 표에 명시된 4개 엔드포인트를 그대로 구현: `GET /api/v1/dashboard/summary`(전체 인원·즉시/부분/풀 가동 인원수·이달 종료 예정자·평균 가동률 KPI), `/dept-utilization`(부서별 평균 가동률), `/job-type-distribution`(직무 유형별 인력 분포, 미등록 사원은 별도 그룹), `/utilization-by-type?month=yyyyMM`(RUNNING→+COMMITTED→+PROPOSED 3단계 조직 평균 가동률). `backend/app/repositories/hr_avail_snap.py`에 `active_alloc_rt_subquery`(신규)를 추출해 가동률 계산 API(`compute_availability`)와 동일한 산정 조건을 대시보드 집계에서도 재사용, `backend/app/repositories/dashboard.py`(신규)·`backend/app/schemas/dashboard.py`(신규)·`backend/app/api/v1/dashboard.py`(신규, `require_permission("dashboard", "view")` — 기존 PERM_JSON `dashboard.view`가 6개 역할 전부 허용이라 그대로 재사용) 작성. **중요한 설계 결정**: 화면 설계서는 데이터 소스를 `HR_AVAIL_SNAP` 테이블로 명시하지만 스냅샷 생성 배치(`HR_AVAIL_SNAP_GEN`, Phase 7)가 아직 없어 테이블이 항상 비어 있으므로, 동일 산정 로직을 사원 단위로 실시간 계산해 대체 — 결과값은 스펙상 정확하나 매 요청마다 재계산하므로 Phase 7 배치 도입 후 스냅샷 기반으로 전환 검토가 필요함을 §9 리스크로 기록. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 부서 2개·프로젝트·사원 3명(0%/50%/100%)의 임시 데이터로 4개 엔드포인트 응답을 수기 계산과 대조해 전부 정확히 일치함을 확인(KPI 카드 합계, 부서별 평균, 직무 미등록 그룹핑, 3단계 월별 집계 비율). 잘못된 `month` 형식 422, 무인증 401도 확인. 검증에 사용한 임시 데이터는 검증 직후 전부 삭제. Phase 3 진행률 89%→94%로 갱신, §11 "대시보드 집계 API" 완료 체크, §9 리스크 1건 추가, §8 큐에서 완료 항목 제거 및 재번호(1)
- **Excel Export API 구현 — Import는 별도 분리 (§8 다음 작업 1번)** — `[DESIGN]HRM_Screen_Design.md` SCR-003(사원 목록) "Excel Import/Export 컬럼 매핑" 및 "연동 API" 표에 명시된 `GET /api/v1/employees/export`를 구현. `backend/app/repositories/hr_empl_mst.py`에 `list_employees_for_export`(신규, 필터는 `list_employees`와 동일하나 페이지네이션 없이 전체 반환) 및 보유역할(`HR_EMPL_ROLE_REL`+`HR_JIKMU_MST.JIKMU_CD`)·주요기술+숙련도(`HR_EMPL_SKILL_REL`+`HR_SKILL_MST`)를 사원별로 `string_agg`로 집계하는 헬퍼 2종 추가(N:M 관계라 콤마로 이어붙임 — 숙련도는 원본 Excel 서식 자체가 "전체 기술에 동일 숙련도" 한 칸만 두는 손실 매핑이라 여러 기술 중 최댓값을 대표로 사용, 사유 주석 명시). `backend/app/api/v1/employees.py`에 `GET /employees/export`(신규) 추가 — `openpyxl`(신규 의존성, `requirements.txt`에 추가)로 설계서 컬럼 순서(사번/성명/팀/직급/보유역할/주요기술/숙련도/입사일/재직상태/휴대폰번호) 그대로 `.xlsx` 생성, `StreamingResponse`로 다운로드 응답. 재직상태는 `EMPL_STAT_CD`(ACTIVE/LEAVE/RETIRED)를 재직/휴직/퇴직으로 매핑(설계서는 재직/퇴직 2종만 예시로 들었으나 실제 코드 값이 3종이라 합리적으로 확장, 사유 주석 명시). `require_permission("employees", "excel")`을 재사용(기존 PERM_JSON `employees.excel`이 이미 ADMIN/HR_MGR만 허용 — 설계서의 "Excel 가져오기 권한: A H" 원칙과 동일하게 적용), `record_audit`으로 `ACT_CD='EXPORT'` 기록(내보낸 행 수 포함). **Import는 이번 범위에서 제외**: 팀/직급/역할/기술을 명칭으로 조회해 FK로 변환, `EMPL_NO` 기준 신규/수정 upsert, 행 단위 검증 실패 시 전체 롤백 vs 부분 성공 처리 등 여러 설계 판단이 필요해 백로그 별도 항목으로 분리(§9 참고). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 부서·기술·역할이 연결된 임시 사원 1명으로 `.xlsx` 다운로드 후 `openpyxl`로 실제 내용을 열어 10개 컬럼 전부 정확한 값(팀명/직급명/기술명/숙련도/재직상태 한글 라벨 등)으로 채워짐을 확인, `excel` 권한 없는 VIEWER 역할 403, 무인증 401, `SYS_AUDIT_LOG`에 `ACT_CD='EXPORT'` 기록 확인. 검증에 사용한 임시 데이터는 검증 직후 전부 삭제. §11 "Excel Import/Export API" 항목을 "Export만 완료, Import 미구현"으로 설명 갱신(체크박스는 미완료 유지 — 항목 전체가 완료된 것은 아니므로), §9 리스크 1건 추가(Import 설계 판단 필요), §8 큐를 Import 전용 항목으로 재구성
- **백로그 문서 정정 — "로그인 JWT API 연동" 항목 신규 추가 (사용자 요청)** — 사용자가 "백로그 구현 리스트에 항목이 없다면 로그인 JWT API 연동 내용을 추가해달라"고 요청. §4 Phase 4·§11 프론트엔드 체크리스트·§8 다음 작업 큐 전체를 확인한 결과, 백엔드 JWT 인증 API(`POST /api/v1/auth/{login,refresh,logout}`)는 2026-07-03에 이미 완료·검증되었으나 프론트엔드가 이를 실제로 호출하도록 연동하는 작업 자체를 가리키는 백로그 항목이 어디에도 없었음을 확인(§6 "인증 방식" 행과 §11 "로그인 화면 구현" 항목 비고에 "JWT API 연동 전까지 대체"라는 언급만 있었고, 별도 추적 항목은 부재) — 신규 발견된 누락 항목으로 추가. §4 Phase 4 "주요 작업" 표에 "로그인 JWT API 연동" 행 신규 추가(예정), §11 프론트엔드 체크리스트에 동일 항목 미완료로 신규 추가, §8 다음 작업 큐에 2번 항목으로 추가(1번 Excel Import 다음 순서). 실질적인 코드 변경은 없음(백로그 문서 정정만 수행)
- **로그인 JWT API 연동 구현 (§8 다음 작업 2번)** — 앞서 백로그에 신규 추가한 항목을 이어서 구현. `frontend/lib/auth.ts`를 localStorage 세션 마커(`'1'`) 저장 방식에서 실제 액세스/리프레시 토큰 저장 방식으로 전면 교체 — `login(userLoginId, password)`(신규, `POST /api/v1/auth/login` 호출, 401 시 "아이디 또는 비밀번호가 올바르지 않습니다" 안내, 네트워크 오류 별도 안내), `logout()`(신규, `POST /api/v1/auth/logout`을 최선 노력으로 호출 후 클라이언트 세션 삭제 — 실패해도 사용자 경험에 영향 없도록 처리), `getAccessToken()`(신규, 향후 인증이 필요한 API 호출에 재사용 가능) 추가. `isAuthenticated()`는 기존과 동일한 시그니처를 유지해 `app-shell.tsx`의 인증 가드 코드는 변경하지 않음(영향 범위 최소화). `frontend/app/login/page.tsx`의 `setTimeout` 목업 로직을 `login()` 실제 호출로 교체, 더 이상 사실이 아닌 "데모 계정: admin / 아무 비밀번호" 안내 문구 제거. `frontend/components/layout/top-nav.tsx`의 로그아웃 메뉴를 `logout()` 비동기 호출로 교체. **중요한 설계 결정**: 토큰 저장 방식은 설계서가 목표로 하는 HttpOnly Cookie 대신 기존 아키텍처(localStorage)를 그대로 유지 — HttpOnly Cookie 전환은 백엔드가 로그인 응답을 `Set-Cookie`로 내려주도록 별도 API 변경이 필요해 이번 최소 단위 범위에서 다루지 않고 §9 리스크로 기록(XSS 시 토큰 탈취 위험이 HttpOnly Cookie보다 높음을 명시). **실 서버 컨테이너에서 실제 렌더링 검증**: `sg docker -c "docker compose up -d --build web"`로 재빌드해 TypeScript/Next.js 빌드 정상 통과 확인(로컬 Node 16 제약 대체 검증), `/login` 200 정상 응답, 컴파일된 클라이언트 번들에서 `USER_LGID` 필드가 포함된 로그인 요청 페이로드가 실제로 존재함을 확인해 목업 코드가 실 API 호출로 정상 교체되었음을 검증. 브라우저 기반 실제 로그인 클릭 테스트는 headless 브라우저 도구가 없어 미실시 — 번들 코드 검증으로 대체 (아래 검증 결과 참조). §4/§11 "로그인 JWT API 연동" 항목 완료 체크, §6 "인증 방식" 진행 상황 갱신, §9 리스크 1건 추가, §8 큐에서 완료 항목 제거(Excel Import만 남음)
- **Excel Import API 구현 — 사용자 확정 정책 반영 (§8 다음 작업 1번)** — 사용자가 Import 정책을 확정: (1) 팀/직급/역할/기술 명칭이 마스터에 없으면 자동 생성·행 스킵 없이 전체 Import를 실패 처리(행 번호/컬럼/입력값/사유 상세 반환), (2) `EMPL_NO` 기준 Upsert(파일 내부 중복 시 전체 실패), (3) 검증 오류가 1건이라도 있으면 DB 변경 없이 실패 응답, 전체 통과 시에만 단일 트랜잭션으로 반영. `backend/app/services/employee_import.py`(신규) — `parse_and_validate`(Excel 헤더/필수 컬럼/파일 내 사번 중복/부서·직급·역할(JIKMU_CD)·기술 명칭의 마스터 존재 여부/숙련도 범위(1~5)/입사일 형식/재직상태 라벨을 전부 검사해 오류가 하나라도 있으면 `EmployeeImportValidationError` 발생 — 이 시점까지 DB에는 아무것도 쓰지 않음), `apply_import`(검증 통과 행만 받아 사번 기준 Upsert, 보유역할·기술스택은 사원별로 Import 파일 기준으로 전체 동기화(파일에 없는 기존 관계 삭제) 후 단일 트랜잭션 커밋, 예외 발생 시 rollback). `backend/app/api/v1/employees.py`에 `POST /employees/import`(신규, `UploadFile`, `require_permission("employees", "excel")` 재사용) 추가 — 검증 실패 시 422(총 행 수/오류 건수/행별 오류 목록), 성공 시 200(총 행 수/신규·수정·역할·기술 처리 건수), `record_audit`으로 `ACT_CD='IMPORT'` 기록. `python-multipart`(신규 의존성, 파일 업로드에 필요) 추가. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 4가지 시나리오 전부 확인 — ① 정상 파일(신규 사원 1명, 역할·기술 연결 포함) 등록 성공, ② 존재하지 않는 부서명 포함 파일 422(오류 상세 정확), ③ 파일 내 사번 중복 422, ④ 기존 사번 재업로드 시 이름/전화번호 수정 + 역할·기술 연결이 새 파일 기준으로 정확히 동기화(비어있는 파일 재업로드 시 기존 연결 0건으로 삭제)됨을 `psql`로 직접 확인. `excel` 권한 없는 VIEWER 403, 무인증 401, `SYS_AUDIT_LOG`에 `ACT_CD='IMPORT'` 2건(성공한 두 번의 업로드) 정상 기록 확인. 실패한 두 시나리오(②③)는 DB에 아무 흔적도 남지 않음을 확인. 검증에 사용한 임시 데이터는 검증 직후 전부 삭제. §4 "Excel Import/Export API" 완료로 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거. **Phase 3 재점검**: "주요 작업" 표 전 항목이 완료되어 진행률을 100%로 갱신했으나, §4 Phase 3 "완료 기준" 4개 항목 중 "Pytest 단위 테스트 핵심 API 커버"가 전혀 작성되지 않아 미충족 상태임을 재확인 — Phase 3을 "완료"로 선언하지 않고 §8 다음 작업 1순위를 "Pytest 단위 테스트 스위트 구축"으로 재구성, §9 리스크 1건 추가
- **버그 수정 — `NEXT_PUBLIC_API_BASE_URL`이 프론트엔드 Docker 빌드에 반영되지 않던 문제 (사용자 보고)** — 사용자가 "pgcrypto로 admin 계정을 만들었는데 프론트엔드 로그인 화면에서 로그인이 안 된다"고 보고. 먼저 백엔드 `POST /api/v1/auth/login`을 직접 호출·`verify_password()` 단위 검증으로 pgcrypto bcrypt 해시 자체는 문제없음을 확인(정상 200 응답)했으나, "프론트엔드 화면에서 시도했다"는 추가 정보로 원인을 프론트엔드 쪽으로 재조사. `NEXT_PUBLIC_API_BASE_URL`은 Next.js가 `next build` 시점에 클라이언트 번들로 인라인하는 값인데, `docker-compose.yml`의 `web` 서비스는 `env_file`(컨테이너 런타임 주입)만 사용하고 이미지 빌드에 필요한 `build.args`가 없었으며 `frontend/Dockerfile`에도 해당 `ARG` 선언이 없어, 빌드된 클라이언트 번들에 백엔드 URL이 전혀 포함되지 않고 있었음을 발견 — 로그인 요청이 상대 경로(`/api/v1/auth/login`)로 나가 Next.js 서버(3030) 자신에 도달해 실패하는 구조였다. 이 버그는 Phase 1에서 해당 환경변수를 "완료"로 표시한 시점부터 잠재해 있었으나 그동안 화면이 목데이터만 사용해 드러나지 않았고, 직전 턴(§7 v4.9)의 로그인 JWT 연동 검증에서도 컴파일된 번들에 `USER_LGID` 필드 존재만 확인하고 baseURL 인라인 여부까지는 검증하지 못해 놓쳤음을 자체 확인. `docker-compose.yml`의 `web.build.args`에 `NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL}` 추가(프로젝트 루트 `.env`를 Compose가 자동 로드해 값 주입), `frontend/Dockerfile`의 builder 스테이지에 `ARG NEXT_PUBLIC_API_BASE_URL` + `ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL` 추가. **실 서버 컨테이너에서 실제 검증**: 재빌드 후 컴파일된 클라이언트 번들에 `http://localhost:8000`이 정상 포함됨을 확인, `curl`로 브라우저와 동일하게 `Origin: http://localhost:3030` 헤더를 포함한 CORS 프리플라이트(OPTIONS) 및 실제 로그인 요청이 전부 정상(200, 토큰 발급) 처리됨을 확인. `.env`/DESIGN 파일은 수정하지 않음(설정값은 기존 `.env`에 이미 존재, Docker Compose/Dockerfile의 빌드 연결부만 수정). §9 리스크에 "해소"로 기록, §11 "NEXT_PUBLIC_API_BASE_URL 환경변수 설정"/"API Client" 항목 설명 갱신
- **Pytest 단위 테스트 스위트 구축 — Phase 3 정식 완료 (§8 다음 작업 1번)** — `backend/requirements.txt`에 `pytest`/`httpx` 신규 추가, `backend/pytest.ini`(신규, `pythonpath = .`로 `import app...` 해석) 작성. `backend/tests/conftest.py`(신규)에 실 DB 연결 하나를 열어 외부 트랜잭션을 시작하고 세션은 `join_transaction_mode="create_savepoint"`로 생성하는 표준 격리 패턴 구현 — 애플리케이션 코드가 각 API 호출 안에서 `db.commit()`을 호출해도 SAVEPOINT만 커밋되고, 테스트 종료 시 외부 트랜잭션을 롤백해 실 DB에는 어떤 흔적도 남기지 않는다(별도 테스트 DB 없이도 안전하게 반복 실행 가능). `app.dependency_overrides[get_db]`로 FastAPI 앱의 DB 세션을 테스트 세션으로 교체하는 `client` 픽스처, `SYS_ROLE_MST`의 기존 ADMIN/VIEWER Seed를 그대로 활용하는 `admin_token`/`viewer_token` 픽스처 작성. 테스트 파일 4종(`test_health.py`, `test_auth.py`, `test_employees.py`, `test_assignments.py`) 총 16개 케이스 작성 — `/health`, 로그인 성공/실패/미존재 사용자, 토큰 갱신, 토큰 타입 오용 거부, 인증 없는/위조 토큰 접근 거부, 사원 생성·조회·수정·퇴직·재퇴직 409·중복 사번 409·미존재 404, RBAC(VIEWER는 조회 가능·생성 403), 투입 관리 ALLOC_RT 100% 초과 거부(409)·정확히 100% 허용(201)·취소된 투입 재집계 제외 커버. **실 서버 컨테이너에서 실제 실행**: 이미지 재빌드 후 `pytest -v` 16개 전부 통과 확인, 실행 직후 `psql`로 `SYS_USER_MST`/`HR_DEPT_MST`/`PJT_MST`/`HR_EMPL_MST`에 `pytest_%`/`PYTEST%` 패턴의 잔여 데이터가 0건임을 확인해 트랜잭션 롤백 격리가 실제로 동작함을 검증. §4 Phase 3 "완료 기준" 4개 항목(핵심 CRUD 응답 확인/JWT·RBAC 동작 확인/감사 로그 기록 확인/Pytest 커버)이 전부 충족되어 **Phase 3을 정식 완료(개발 상태 "완료", 진행률 100%)로 전환**, §3 전체 로드맵 표 갱신, §9 리스크 "해소" 처리, §8 큐를 Phase 3 완료로 다음 순서인 Phase 4(Next.js) 잔여 항목("공통 레이아웃·네비게이션 권한별 메뉴 제어", "대시보드 화면 구현")으로 재구성
- **프론트엔드 전체 한글 폰트를 Noto Sans KR로 변경 (사용자 요청)** — `frontend/app/layout.tsx`의 본문 폰트를 `next/font/google`의 `Geist`(라틴 전용)에서 `Noto_Sans_KR`(subsets `latin`+`korean`, weight 400/500/600/700)로 교체 — 화면 대부분이 한글이라 한글 글리프를 지원하지 않는 라틴 전용 폰트 대신 한글 최적화 폰트로 전환. CSS 변수명(`--font-geist-sans`)은 그대로 유지해 `globals.css`의 `--font-sans` 매핑 등 다른 파일 변경을 최소화(폴백 폰트명만 `'Geist Fallback'`→`'Noto Sans KR Fallback'`으로 갱신). 코드/숫자용 모노스페이스 폰트(`Geist Mono`)는 변경하지 않음(한글 폰트 요청 범위 밖). **실 서버 컨테이너에서 실제 렌더링 검증**: `sg docker -c "docker compose up -d --build web"`로 재빌드(TypeScript/Next.js 빌드 정상 통과 확인 — 로컬 환경 Node 16 제약으로 못했던 빌드 검증을 실 서버에서 대체 수행), `/login` 200 정상 응답, 실제 서빙된 CSS에서 `font-family: Noto Sans KR, Noto Sans KR Fallback`이 `--font-geist-sans` 변수에 정상 매핑되어 적용됨을 확인, `Geist Mono`는 그대로 유지됨을 확인. 백로그에 해당 전용 체크리스트 항목이 없어 Phase 진행률 변경 없음(§7 완료 내역에만 기록)
- **대시보드 집계 API — 프론트엔드 목데이터 기반 4개 엔드포인트 추가 (사용자 요청)** — 사용자가 "현재 frontend에 mock 데이터로 구현되어 있는 dashboard를 참고해서 필요한 API를 구현"을 요청. `frontend/app/(app)/dashboard/page.tsx`와 `frontend/lib/mock-data.ts`를 확인한 결과, 화면이 이미 SCR-002 설계서 표에 없던 4개 위젯(데이터 품질 점검·이달 투입 종료 예정 상세 목록·최근 입사자·월별 인력 추이)을 목데이터로 표시하고 있음을 확인 — 앞서 구현한 4개 엔드포인트(설계서 명시분)로는 커버되지 않는 부분이라 추가로 구현. `backend/app/repositories/dashboard.py`에 `get_data_quality`(재직 사원 중 기술/직무 미등록 수, `ALLOC_RT` 합계 100% 초과 사원 수), `get_ending_this_month`(이번 달 종료 예정 투입 상세 목록 — 사원명/부서명/프로젝트명/종료일/투입률), `get_recent_employees`(최근 입사자, `HIRE_DT` 내림차순), `get_headcount_trend`(월별 재직 인원/입사/퇴사 추이, 개월 수 파라미터화) 4개 함수 추가. `backend/app/schemas/dashboard.py`·`backend/app/api/v1/dashboard.py`에 대응 스키마·엔드포인트(`GET /api/v1/dashboard/{data-quality,ending-this-month,recent-employees,headcount-trend}`) 추가, 기존과 동일하게 `require_permission("dashboard", "view")` 적용. 100% 초과 데이터 점검은 등록/수정 API에서 이미 저장 차단하지만(§9 참조) 기존 Excel 이관 데이터 예외(`AVAILABILITY_CALC_SPEC.md` §5)를 대비해 별도로 재점검하도록 구현. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 사원 3명(기술/직무 미등록 1명, 정상 1명 — 레거시 100% 초과 투입 직접 삽입, 이번 달 퇴직 1명)의 임시 데이터로 4개 엔드포인트를 수기 계산과 대조 — 데이터 품질(기술 미등록 1/직무 미등록 1/초과 1), 이달 종료 예정 1건, 최근 입사자 2명(퇴직자 제외), 3개월 인력 추이(입사 1·퇴사 1 반영) 전부 정확히 일치함을 확인. 검증에 사용한 임시 데이터는 검증 직후 전부 삭제. §11 "대시보드 집계 API" 항목 설명에 8개 엔드포인트 전체 반영, 별도 리스크 추가 없음(기존 §9 "대시보드 API가 HR_AVAIL_SNAP 대신 실시간 계산 사용" 리스크와 동일 원칙 적용)
- **공통 레이아웃·네비게이션 — 권한별 메뉴 제어 구현 (§8 다음 작업 1번)** — 사이드바 메뉴를 로그인 사용자의 `SYS_ROLE_MST.PERM_JSON` 기준으로 필터링하는 기능을 구현. 프론트엔드에는 로그인 성공 후 현재 사용자의 역할·권한을 조회할 방법이 없어(토큰에는 `role_id`만 있고 `PERM_JSON`은 없음), `backend/app/api/v1/auth.py`에 `GET /api/v1/auth/me`(신규, 기존 `get_current_user` 의존성만 사용 — 별도 권한 검사 없이 인증된 사용자면 자신의 정보 조회 가능) 및 `backend/app/schemas/auth.py`에 `MeOut`(신규, `USER_LGID`/`ROLE_CD`/`ROLE_NM`/`PERM_JSON` 반환) 추가. `frontend/lib/nav.ts`의 `NavItem`에 `permKey`(선택, `PERM_JSON.screens`의 화면 키) 필드 추가해 각 메뉴를 대응 화면 키에 매핑(대시보드→`dashboard`, 사원 관리→`employees` 등), `filterNavByPermissions` 헬퍼(신규, `permKey`가 없는 항목은 항상 노출, 있으면 `screens[permKey].view===true`인 것만 통과) 추가. `frontend/lib/auth.ts`에 `getMe()`(신규, `/auth/me` 호출, 실패 시 `null` 반환 — 권한 조회 실패가 메뉴를 숨기는 방향으로 작동하지 않도록 설계, 실제 접근 차단은 각 API의 RBAC가 담당) 추가. `frontend/components/layout/app-shell.tsx`에서 인증 확인 직후 `getMe()`를 호출해 `PERM_JSON`을 `Sidebar`(데스크톱·모바일 드로어 두 곳 모두)에 전달, `frontend/components/layout/sidebar.tsx`는 전달받은 `permJson`으로 `mainNav`/`bottomNav`를 필터링해 렌더링. **실 서버 컨테이너에서 실제 검증**: 백엔드 재빌드 후 실제 `admin` 계정으로 `GET /auth/me` 호출해 `ROLE_CD=ADMIN`과 `PERM_JSON` 전체가 정상 반환됨을 확인, 무인증 호출 401 확인. `backend/tests/test_auth.py`에 `test_me_returns_current_user_and_perm_json`/`test_me_requires_auth` 2개 케이스 추가해 pytest 스위트를 16개→18개로 확장, 전부 통과 확인. 프론트엔드는 `docker compose up -d --build web` 재빌드 후 컴파일된 클라이언트 번들에 `/auth/me` 호출 코드가 포함됨을 확인. §4 Phase 4 "공통 레이아웃·네비게이션" 항목을 진행 중→완료로 갱신(Phase 4 진행률 31%→38%), §11 동일 항목 완료 체크, §8 큐에서 완료 항목 제거(대시보드 화면 구현만 남음)
- **대시보드 화면 구현 — 목데이터를 백엔드 8개 API로 전량 교체 (§8 다음 작업 1번)** — 기존 `frontend/app/(app)/dashboard/page.tsx`가 `lib/mock-data.ts`를 직접 참조하던 것을 실제 백엔드 API 호출로 전면 교체. 선행 작업으로 `HeadcountChart`/`JobTypeDonut`/`DeptUtilizationChart` 3개 차트 컴포넌트가 각각 목데이터를 내부에서 직접 import하던 구조를 `data` prop을 받는 구조로 리팩터링(export 타입 `HeadcountTrendPoint`/`JobTypeDistributionPoint`/`DeptUtilizationPoint` 신규 추가), 같은 컴포넌트를 소비하던 `frontend/app/(app)/reports/page.tsx`(이번 작업 범위 밖, 목데이터 유지)도 호환을 위해 `data` prop을 명시적으로 전달하도록 함께 수정. 인증이 필요한 API 호출을 화면마다 반복하지 않도록 `frontend/lib/api.ts`(신규) — `apiGet<T>(path)` 공통 헬퍼(저장된 액세스 토큰을 `Authorization` 헤더로 첨부, 실패 시 `ApiError` throw) 추가. `dashboard/page.tsx`를 `'use client'` + `useEffect`/`useState` 기반으로 재작성해 `GET /api/v1/dashboard/{summary,dept-utilization,job-type-distribution,utilization-by-type,data-quality,ending-this-month,recent-employees,headcount-trend}` 8개 엔드포인트를 병렬 호출(`Promise.all`), 응답을 각 위젯이 기대하는 형태로 매핑(부서 가동률 반올림, 직무 분포 필드명 변환, 추이 월(`yyyyMM`)을 `MM.DD` 표시 형식으로 변환). 백엔드에 실제 데이터가 없어 값이 0/null인 상황(`avg_utilization_rate: null` 등)을 대비해 화면에 이미 존재하던 조건부 렌더링을 그대로 활용, 별도 목업/폴백 값을 추가하지 않음(설계 원칙상 실 데이터 없음을 있는 그대로 표시). 로딩 중/에러 상태 UI 추가(기존 화면에 없던 것을 API 연동에 따라 신규로 최소 추가). **실 서버 컨테이너에서 실제 검증**: `docker compose up -d --build web` 재빌드 성공(`/dashboard`가 `○ (Static)`로 정상 프리렌더되어 TypeScript 컴파일 오류 없음을 확인), `curl http://localhost:3030/dashboard` 200 확인, 컴파일된 클라이언트 번들에 `dashboard/summary` 문자열이 포함되어 목업 코드가 실제 API 호출로 교체되었음을 확인, 실 `admin` 계정으로 로그인해 얻은 토큰으로 8개 엔드포인트를 전부 직접 curl 호출해 응답 JSON 구조가 `page.tsx`에 정의한 TypeScript 인터페이스와 정확히 일치함을 확인(현재 시드 데이터 없어 값은 0/빈 배열이나 구조는 유효). §4 Phase 4 "대시보드 화면 구현" 항목 완료로 갱신(Phase 4 진행률 38%→44%), §3 전체 로드맵 표 Phase 4 진행률 동일 갱신, §11 동일 항목 완료 체크, §8 큐에서 완료 항목 제거하고 Phase 4 "주요 작업" 표에서 아직 미완료인 나머지 항목들로 재구성
- **사원 상세 화면 구현 — 목데이터 스캐폴딩을 실 API로 연동 (§8 다음 작업 1번)** — 기존 저장소에 이미 존재하던 `frontend/app/(app)/employees/[id]/page.tsx`(초기 프로토타입 스캐폴딩, 기본정보/보유기술/투입이력/변경이력 4개 탭 구조와 정보수정 모달까지 UI로는 이미 구현되어 있었으나 전부 `lib/mock-data.ts` 기반)를 실제 백엔드 API 호출로 재작성. 사원 단건 조회 API가 없어(목록/수정/삭제만 존재) `backend/app/api/v1/employees.py`에 `GET /employees/{empl_id}`(신규, 기존 `get_employee` 리포지토리 함수 재사용, `require_permission("employees","view")`, 404 처리) 추가 — 기술 조회(`GET /employee-skills?empl_id=`)와 투입 이력 조회(`GET /assignments?empl_id=`)는 이미 구현되어 있어 별도 백엔드 변경 없이 그대로 재사용. 프론트엔드는 사원 기본정보·부서명·직급명·직무유형명·사원기술(기술 마스터와 조인해 이름/그룹 표시)·투입 이력(프로젝트 마스터와 조인해 이름 표시)을 병렬로 조회해 3개 탭(기본정보/보유기술/투입이력)에 실 데이터로 렌더링, 현재 가동률은 `ASGN_STAT_CD='ACTIVE'`인 투입 건의 `ALLOC_RT` 합계로 계산. **범위를 의도적으로 축소한 부분**: (1) 정보수정·기술추가·퇴직처리 버튼은 이번 범위에서 제외 — 기존 `EmployeeFormModal`이 mock `Employee` 타입에 강하게 결합되어 있어 실 API(`PATCH`) 스키마로 재작성하려면 폼 전체를 다시 설계해야 해 "최소 단위" 원칙에 따라 조회 전용으로 우선 제공하고 후속 작업으로 분리(§9 리스크 추가), (2) "변경 이력" 탭은 설계서가 요구하는 `GET /api/v1/audit-logs?target_id=` 감사 로그 조회 API 자체가 백엔드에 아직 없어 이번 범위에서 탭을 제외(§9 리스크 추가). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 부서 마스터가 비어 있어(`HR_DEPT_MST` 0건 — Seed 미완료 상태, §9 참조) 검증용 임시 부서 1건을 직접 SQL로 추가하고, 사원 2명(기본 정보만, 기술+투입 이력 포함)을 API로 등록해 `GET /employees/{empl_id}` 200 정상 응답, 존재하지 않는 ID 404 확인, `employee-skills`/`assignments` 응답 구조를 프론트엔드 타입과 대조해 일치 확인(투입 이력 응답이 `PaginatedResponse` 래퍼(`{total, items}`)임을 뒤늦게 발견해 프론트엔드 파싱 버그를 수정 — 최초 구현 시 배열로 잘못 가정했던 점 수정 후 재빌드로 검증), `/employees/{empl_id}` 페이지 200 렌더링 확인. 검증에 사용한 임시 부서·사원·사원기술 데이터는 검증 직후 전부 SQL로 삭제(사원 삭제 API는 소프트 삭제(퇴직 처리)만 지원해 실제 행 제거는 SQL로 수행). `backend/tests/test_employees.py`에 상세 조회 성공/404/VIEWER 조회 가능 3개 케이스 추가(pytest 18→21개 전부 통과). §4 Phase 4 "사원 상세 화면 구현" 항목 완료로 갱신(진행률 44%→50%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거 — 큐 재구성 중 지난 턴(v5.4)에서 §4 표의 "설정 화면 구현"·"Excel Import/Export UI 구현" 2개 항목이 누락되었던 것도 함께 바로잡음

---

## 8. 다음 작업

> Rolling Backlog / Next Action Queue — 누적 완료 목록이 아니라 "지금부터 수행할 작업"만 유지한다.
> 완료된 작업은 이 섹션에 남기지 않고 §7 개발 완료 내역과 §11 MVP 구현 체크리스트에만 기록한다.

- [ ] 1. 기술 관리 화면 구현 (`/skills`, `HR_SKILL_MST`)
- [ ] 2. 직무 유형 관리 화면 구현 (`/job-types`, `HR_JIKMU_MST`)
- [ ] 3. 프로젝트 목록/상세 화면 구현 (`/projects`, `/projects/[id]`)
- [ ] 4. 투입 관리 화면 구현 (`/assignments`, `PJT_ASGN_HIS`)
- [ ] 5. 가동 가능 인력 조회 화면 구현 (`/availability` — 직무 유형 필터 포함)
- [ ] 6. 리소스 추천 화면 구현 (`/recommendations`, `PJT_RCMD_RSLT`)
- [ ] 7. AI Chat 화면 구현 (`/ai-chat`)
- [ ] 8. 리포트 화면 구현 (`/reports`)
- [ ] 9. 설정 화면 구현 (`/settings/users`, `/settings/audit-logs`)
- [ ] 10. Excel Import/Export UI 구현

> 참고: "사원 상세 화면 구현"은 2026-07-03에 완료되어(§7, §11 참조) 이 큐에서 제외했다. 지난 턴에 §4 Phase 4 표의 "설정 화면 구현"·"Excel Import/Export UI 구현" 항목이 큐 재구성에서 누락되었던 것을 이번에 바로잡아 9·10번으로 추가했다.

> 참고: "대시보드 화면 구현"은 2026-07-03에 완료되어(§7, §11 참조) 이 큐에서 제외하고, §4 Phase 4 "주요 작업" 표에서 아직 "예정"으로 남은 나머지 항목들로 큐를 재구성했다.

> 참고: "공통 레이아웃·네비게이션 권한별 메뉴 제어"는 2026-07-03에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

> 참고: "Excel Export API 구현(`GET /api/v1/employees/export`)", "Excel Import API 구현(`POST /api/v1/employees/import`)", "로그인 JWT API 연동", "Pytest 단위 테스트 스위트 구축"은 2026-07-03에 완료되어(§7, §11 참조) 이 큐에서 제외했다. Import 정책은 사용자 확정 사항(마스터 미존재 시 전체 실패, `EMPL_NO` 기준 Upsert, 부분 실패 시 전체 롤백)을 그대로 반영했다.

> 참고: Phase 3(FastAPI 백엔드 구축)이 2026-07-03에 정식 완료되어, §8 큐를 §3/§4 로드맵상 다음 순서인 Phase 4(Next.js 웹 클라이언트) "주요 작업" 표에서 아직 미완료인 항목들로 재구성했다.

> 참고: "부서/직급/직무 코드 조회 API", "Pydantic v2 스키마 작성 — 나머지 15개 테이블 도메인", "기술 CRUD API 구현(`HR_SKILL_MST`, `HR_EMPL_SKILL_REL`)", "프로젝트 CRUD API 구현(`PJT_MST`)", "투입 관리 API 구현(`PJT_ASGN_HIS`)", "JWT 인증 API 구현(`SYS_USER_MST` 기반)", "`SYS_AUDIT_LOG` 감사 로그 미들웨어 구현", "RBAC 권한 미들웨어 구현(`SYS_ROLE_MST` 기반)", "사원 퇴직 처리 API 구현", "페이지네이션 공통 처리 구현", "OpenAPI 문서 확인", "가동률 계산 API 구현(`HR_AVAIL_SNAP`)", "대시보드 집계 API 구현"은 2026-07-03에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

> 참고: §8 큐가 이전 항목 완료로 비어, §4 Phase 3 "주요 작업" 표에서 아직 "예정"으로 남은 항목 3개(표 나열 순서 그대로)를 새 큐로 구성했다. 실제 착수 전 우선순위(예: Phase 4 프론트엔드 착수를 먼저 할지)는 재확인 가능.

> 참고: 순서는 §4 Phase 3 "주요 작업" 표 나열 순서를 기준으로 구성했다. 실제 우선순위(예: 인증을 CRUD API보다 먼저)는 착수 전 재확인 가능.

> 참고: `HR_EMPL_ROLE_REL`, `HR_AVAIL_SNAP`, `PJT_RSRC_REQ` 모델·마이그레이션은 2026-07-03에 이미 작성 완료되어(§7, §11 참조) 이 큐에서 제외했다. 실 DB 적용 검증(5번)에서 세 테이블도 함께 확인 대상이다.

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
| `POSTGRES_PASSWORD` 노출 이력 (실 배포 트러블슈팅 중 채팅에 평문 공유됨) | 중간 | 해소 | 사용자가 `.env`의 `POSTGRES_PASSWORD`/`DATABASE_URL` 값을 즉시 교체(로테이션) 완료 확인 | 2026-07-03 |
| UFW `5442`(PostgreSQL) 내부망 제한 규칙 미확인 | 낮음 | 해소 | UFW 규칙 대신 `docker-compose.yml`의 `db` 서비스 포트를 `127.0.0.1:5442:5432`로 바인딩해 외부 인터페이스 노출 자체를 차단(Docker가 UFW보다 우선하는 iptables 규칙을 추가하는 문제 회피) — `localhost`(호스트 로컬)에서만 접속 가능 | 2026-07-03 |
| `PJT_ASGN_HIS` ALLOC_RT 100% 초과 검증 집계 범위 미확정 | 중간 | 주의 | ERD §3.9/설계서 §5.5는 "동일 사원 동일 기간 ALLOC_RT 합계 100% 초과 금지" 원칙만 명시하고 집계 대상 상태(`ASGN_STAT_CD`)를 특정하지 않아, MVP로 `PLANNED`/`ACTIVE`만 집계하고 `CANCELED`/`DONE`은 제외하는 것으로 구현(`backend/app/repositories/pjt_asgn_his.py` 주석 참조). `PROPOSED`(제안중)를 포함한 `ASGN_TYPE_CD` 구분은 이번 검증에 반영하지 않음 — 운영팀 확인 후 필요 시 조건 조정 예정 | 2026-07-03 |
| JWT 로그아웃 서버 측 즉시 무효화 미구현 | 낮음 | 주의 | 현재 JWT는 stateless라 `POST /api/v1/auth/logout`이 클라이언트 측 토큰 폐기만 유도하고, 이미 발급된 액세스/리프레시 토큰은 만료 시각(각 60분/7일)까지 유효하다. RBAC 권한 미들웨어(§8 다음 작업 1번) 구현 시 모든 요청에서 토큰을 검증하는 경로가 생기므로, 그 시점에 Redis(이미 `REDIS_URL`로 연결 가능) 기반 토큰 블랙리스트 도입 여부를 함께 검토 예정 | 2026-07-03 |
| passlib 1.7.4 / bcrypt 최신 버전 비호환 | 높음 | 해소 | `passlib[bcrypt]==1.7.4`가 `bcrypt>=4.1`의 `bcrypt.__about__.__version__` 제거로 인해 비밀번호 해싱 시 `AttributeError`/`ValueError`로 실패하는 상위 호환성 버그 발견 — `backend/requirements.txt`에 `bcrypt==4.0.1` 고정 추가로 해결, 실 서버 컨테이너 재빌드 후 해싱/검증 정상 동작 확인 | 2026-07-03 |
| `departments`/`positions`/`job-types` 화면 권한 키 미정 | 중간 | 해소 | 운영팀 확인 완료(2026-07-03) — 부서(`departments`)/직급(`positions`)은 독립 화면이 아닌 "공통 코드/기준정보"로 취급하기로 확정, 별도 화면 키 대신 `SYS_ROLE_MST.PERM_JSON`에 공통 `codes` 키 추가(`codes.view`는 전 역할 허용, `codes.create`/`update`/`delete`는 ADMIN/HR_MGR만 허용). `GET /api/v1/job-types` 조회도 `codes.view` 정책과 동일하게 전 역할 허용(단, 직무 유형 관리 화면의 등록/수정/삭제는 기존 `job_types.*`(A H 전용) 유지). `backend/app/db/seed/sys_role_mst_seed.py` Seed 갱신 및 Alembic 리비전 `9c1f3a5d2b7e`로 기존 DB의 `PERM_JSON`도 갱신 완료, `backend/app/api/v1/codes.py`(부서/직급/직무 유형 조회 API) 3개 엔드포인트에 `require_permission("codes", "view")` 적용 완료 — 인증 없이 호출 가능하던 상태 제거. `backend/docs/PERMISSION_MATRIX.md`에 `codes` 권한 섹션 추가 | 2026-07-03 |
| 페이지네이션 공통화로 OpenAPI 스키마명 변경 | 낮음 | 주의 | `EmployeeListResponse`/`ProjectListResponse`/`AssignmentListResponse`를 Pydantic 제네릭 `PaginatedResponse[T]`의 타입 별칭으로 전환하면서, 응답 JSON 형태(`total`/`skip`/`limit`/`items`)는 동일하게 유지되지만 `/openapi.json`에 노출되는 스키마명이 `PaginatedResponse_EmployeeOut_` 형태로 바뀜. 프론트엔드는 현재 목데이터 기반이라 실 API 응답 스키마에 의존하지 않아 당장 영향 없음 — 향후 OpenAPI 기반 타입 자동 생성 도구 도입 시 참고 필요 | 2026-07-03 |
| 대시보드 API가 `HR_AVAIL_SNAP` 대신 실시간 계산 사용 | 중간 | 주의 | `[DESIGN]HRM_Screen_Design.md` SCR-002는 KPI 카드·부서별 가동률의 데이터 소스를 `HR_AVAIL_SNAP` 테이블로 명시하지만, 스냅샷 생성 배치 `HR_AVAIL_SNAP_GEN`(Phase 7)이 아직 없어 테이블이 항상 비어 있다. 이에 `backend/app/repositories/dashboard.py`는 가동률 계산 API(`compute_availability`)와 동일한 `AVAILABILITY_CALC_SPEC.md` 로직을 사원 단위로 실시간 재계산해 대체 — 결과값은 스펙상 정확하나, Phase 7 배치 도입 후에는 매일 갱신되는 스냅샷 기반 집계로 전환해 매 요청마다 재계산하지 않도록 성능 개선 검토 필요 | 2026-07-03 |
| Excel Import API 설계 판단 필요 | 중간 | 주의 | `POST /api/v1/employees/import`(SCR-003)는 Export와 달리 (1) 팀/직급/역할/기술을 텍스트 명칭으로 받아 FK로 변환 시 명칭이 마스터에 없는 경우 처리 방식, (2) `EMPL_NO` 기준 신규/수정 upsert 판단 기준, (3) 여러 행 중 일부만 검증 실패했을 때 전체 롤백할지 성공 행만 반영할지 정책이 설계서에 명시되어 있지 않아 임의로 결정하지 않고 별도 백로그 항목(§8)으로 분리해 후속 확인 후 진행 예정 | 2026-07-03 |
| 프론트엔드 JWT 토큰을 localStorage에 저장 (HttpOnly Cookie 미적용) | 중간 | 주의 | 로그인 JWT API 프론트엔드 연동 시 설계서가 목표로 하는 HttpOnly Cookie 방식 대신, 기존 `lib/auth.ts` 아키텍처(localStorage)를 그대로 유지하고 저장 내용만 세션 마커에서 실제 액세스/리프레시 토큰으로 교체하는 MVP 방식을 채택 — HttpOnly Cookie 전환은 백엔드가 로그인 응답을 `Set-Cookie`로 내려주도록 별도 API 변경이 필요해 이번 범위에서 다루지 않음. localStorage 저장은 XSS 공격 시 토큰 탈취 위험이 HttpOnly Cookie보다 높으므로, 정식 운영 전환 전 HttpOnly Cookie·자동 토큰 리프레시 도입 검토 필요 | 2026-07-03 |
| Phase 3 완료 기준 중 Pytest 단위 테스트 미충족 | 중간 | 해소 | §4 Phase 3 "완료 기준" 4개 항목 중 "Pytest 단위 테스트 핵심 API 커버"가 미충족 상태였음 — `backend/tests/`에 16개 단위 테스트 작성으로 해소(2026-07-03). 실 DB에 연결하되 연결 단위 트랜잭션+SAVEPOINT로 격리해 테스트 후 자동 롤백되도록 구성, 실 서버 컨테이너에서 전부 통과 확인. Phase 3을 정식으로 "완료" 처리 | 2026-07-03 |
| `NEXT_PUBLIC_API_BASE_URL`이 프론트엔드 Docker 빌드에 실제 반영되지 않던 버그 | 높음 | 해소 | 사용자가 admin 계정으로 pgcrypto bcrypt 해시를 직접 생성해 로그인을 시도했으나 실패한다고 보고 — 백엔드 `POST /api/v1/auth/login`을 직접 호출해 정상 동작함을 먼저 확인한 뒤, "프론트엔드 로그인 화면에서 시도했다"는 추가 정보를 받아 원인을 재조사. `NEXT_PUBLIC_API_BASE_URL`은 Next.js 빌드 시점(`next build`)에 클라이언트 번들로 인라인되어야 하는 값인데, `docker-compose.yml`의 `web` 서비스가 `env_file`(컨테이너 런타임 주입)만 사용하고 `build.args`가 없어 이미지 빌드 시점에는 이 값이 비어 있었음을 확인(`frontend/Dockerfile`도 `ARG` 선언이 없었음) — 빌드된 클라이언트 번들에 백엔드 URL이 전혀 포함되어 있지 않아, 로그인 요청이 상대 경로(`/api/v1/auth/login`)로 나가 Next.js 서버(3030) 자신에 부딪혀 실패하는 구조였다. `docker-compose.yml`의 `web.build`에 `args: {NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL}}` 추가, `frontend/Dockerfile`의 builder 스테이지에 `ARG`/`ENV` 선언 추가로 해결. 이 버그는 Phase 1에서 `NEXT_PUBLIC_API_BASE_URL`을 "완료"로 표시한 시점부터 존재했으나 그동안 실제 API 호출이 없어(목데이터 기반) 드러나지 않았고, 로그인 JWT 연동 시점(§7 v4.9)에도 컴파일된 번들에서 `USER_LGID` 필드 존재만 확인했을 뿐 baseURL 인라인 여부까지는 검증하지 못해 놓친 것으로 확인됨 — 재빌드 후 번들에 `http://localhost:8000`이 정상 포함되고, `curl`로 브라우저와 동일한 `Origin` 헤더를 포함한 로그인 요청이 CORS·인증 모두 정상 통과함을 확인 | 2026-07-03 |
| 사원 상세 화면의 정보수정·기술추가·퇴직처리 UI 미구현 | 중간 | 주의 | 사원 상세 화면(SCR-004)을 실 API로 연동하면서 조회(기본정보/보유기술/투입이력) 기능만 구현하고 편집 기능은 제외 — 기존 `EmployeeFormModal`이 mock `Employee` 타입에 강하게 결합되어 있어 실 API(`PATCH /employees/{empl_id}`, `POST/PATCH /employee-skills`, `DELETE /employees/{empl_id}`) 스키마로 재작성하려면 폼 전체 재설계가 필요해 "최소 단위" 원칙에 따라 후속 작업으로 분리. 백엔드 API 자체는 이미 존재하므로 프론트엔드 폼/모달 작업만 남음 | 2026-07-03 |
| 사원 상세 화면 "변경 이력" 탭 미구현 — 감사 로그 조회 API 부재 | 낮음 | 주의 | 설계서(SCR-004)가 요구하는 `GET /api/v1/audit-logs?target_id={empl_id}` 감사 로그 조회 API가 백엔드에 아직 구현되어 있지 않아 사원 상세 화면에서 "변경 이력" 탭을 제외 — `SYS_AUDIT_LOG`에 데이터 자체는 이미 기록되고 있으므로(§7 참조), 조회 전용 API 1개만 추가하면 됨. 다른 화면(프로젝트 상세 등)에서도 동일 API가 필요할 수 있어 공통 작업으로 별도 백로그 항목화 검토 필요 | 2026-07-03 |
| `HR_DEPT_MST`(부서 마스터) Seed 데이터 없음 | 중간 | 주의 | 사원 상세 화면 검증 중 실 DB에 `HR_DEPT_MST`가 0건(부서 코드 미시딩)임을 확인 — `HR_JIKGUP_MST`(직급, 10건)와 `HR_SKILL_MST`(기술, 1건, 비활성)는 일부 존재하나 부서는 전혀 없어 사원 등록·조회 화면에서 부서 필터/표시가 항상 빈 목록으로 나타남. 운영팀 확정 부서 목록 확보 후 Seed 스크립트(`backend/app/db/seed/`) 추가 필요 | 2026-07-03 |
| `hrm-worker` 컨테이너가 재시작 루프 상태 | 중간 | 주의 | 사원 상세 화면 작업 중 `docker compose ps` 확인 과정에서 `hrm-worker` 컨테이너가 `Restarting (0)` 상태로 반복 재기동 중임을 발견 — 이번 작업과 무관한 기존 이슈로 원인 미조사(범위 밖). 백그라운드 배치/추천 작업이 필요한 Phase(§4 이후)에서 워커가 실제로 사용되기 전에 원인 확인 및 조치 필요 | 2026-07-03 |

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
- [x] Docker Compose Plugin 설치 — v2 전환 완료, `Docker Compose version v5.2.0` 확인 (2026-07-03)
- [x] `/App/hrmngr/` 기준 경로 디렉토리 구조 생성
  ```bash
  mkdir -p /App/hrmngr/{backend,frontend,data/postgres,data/redis,backup/postgres,logs}
  ```
- [x] `docker-compose.yml` 작성 (api / web / db / redis / worker 5개 서비스)
- [x] `.env` 파일 작성 및 `.gitignore` 설정 (`.env`, `data/`, `backup/postgres/*.sql.gz`, `logs/` 제외)
- [x] Git Repository 초기화
- [x] 방화벽(UFW) 설정 — OpenSSH(22), 3030, 8000 허용 및 활성화 완료. 5442는 `docker-compose.yml`에서 `127.0.0.1:5442:5432` 바인딩으로 외부 노출 자체를 차단 (2026-07-03)

---

### 데이터베이스 `→ Phase 2`

- [x] PostgreSQL Docker 컨테이너 구성 (외부 포트 **5442** → 내부 5432) — `docker-compose.yml`의 `db` 서비스가 `127.0.0.1:5442:5432`로 바인딩되어 실 서버에서 정상 구동 중임을 `docker compose ps`(`Up (healthy)`, `127.0.0.1:5442->5432/tcp`)로 확인 완료 (Phase 1 완료 시 이미 검증되었으나 체크 표시가 누락되어 있었음 — 2026-07-03 확인 후 반영)
- [x] `/App/hrmngr/data/postgres/` 바인드 마운트 확인 — `docker-compose.yml`에 `./data/postgres:/var/lib/postgresql/data`로 마운트되어 있고, 실 서버 디렉터리에 `pgdata`가 생성되어 16개 테이블 데이터가 정상 저장되어 있음을 확인 완료 (Phase 1 완료 시 이미 검증되었으나 체크 표시가 누락되어 있었음 — 2026-07-03 확인 후 반영)
- [x] Alembic 마이그레이션 환경 구성 (`env.py` 설정) — `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/script.py.mako`, `backend/app/db/base.py`(`Base` 선언) 작성. 실 서버에서 `alembic upgrade head` 정상 실행 확인 완료 (2026-07-03)
- [x] 전체 테이블 생성 (16개, 16/16 모델·마이그레이션 작성 및 실 서버 DB 적용 검증 완료 — `\dt` 결과 16개 테이블 전부 확인, 2026-07-03)
  - [x] `HR_DEPT_MST` — 부서 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_JIKGUP_MST` — 직급 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_JIKMU_MST` — 직무 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_SKILL_MST` — 기술 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_EMPL_MST` — 사원 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_EMPL_SKILL_REL` — 사원기술 연결 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_EMPL_ROLE_REL` — 사원역할 연결 (복수 직무 지원) (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `HR_AVAIL_SNAP` — 가동가능 스냅샷 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `PJT_MST` — 프로젝트 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `PJT_ASGN_HIS` — 투입 이력 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `PJT_RSRC_REQ` — 리소스 요청 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `PJT_RCMD_RSLT` — 추천 결과 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `SYS_USER_MST` — 시스템 사용자 마스터 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `SYS_ROLE_MST` — 역할 마스터 (실 서버 DB 적용 검증 완료, Seed 6종 `SELECT` 확인, 2026-07-03)
  - [x] `SYS_AUDIT_LOG` — 감사 로그 (실 서버 DB 적용 검증 완료, 2026-07-03)
  - [x] `SYS_BATCH_HIS` — 배치 실행 이력 (모델+마이그레이션 작성 및 실 서버 DB 적용 검증 완료, 2026-07-03)
- [x] Seed 데이터 입력: `SYS_ROLE_MST` (6종, MVP 확정 — `backend/app/db/seed/sys_role_mst_seed.py`) + `HR_JIKGUP_MST`(10종) + `HR_JIKMU_MST`(12종) — `SYS_ROLE_MST`는 마이그레이션 `83fc676b952e_create_sys_user_role_audit_tables.py`에 `op.bulk_insert`로 반영, 실 서버 DB에서 6종 전부 정상 삽입 확인 완료(`SELECT` 결과, 2026-07-03). `HR_JIKGUP_MST`/`HR_JIKMU_MST` Seed는 `backend/app/db/seed/hr_jikgup_mst_seed.py`, `hr_jikmu_mst_seed.py` 신규 작성 및 Alembic 리비전 `370c95546556_seed_hr_jikgup_mst_and_hr_jikmu_mst.py`로 반영 완료 — 실 DB 적용도 Phase 2 완료 검증(2026-07-03, `SELECT COUNT(*)`로 10건/12건 확인)에서 검증 완료 (이전에 "미검증"으로 남아있던 문구는 갱신 누락이었음)
- [ ] `HR_SKILL_MST` Seed 입력 — MVP 초안 55건 작성 완료(`backend/app/db/seed/hr_skill_mst_seed.py`), 운영팀 최종 확정 후 실 데이터 반영 예정 (미완료 유지)
- [ ] DB 백업 스크립트 작성 (`/App/hrmngr/backup/backup_db.sh`) 및 crontab 등록 (매일 02:00) — 스크립트 작성 및 수동 실행(`pg_dump` 백업 파일 생성)은 완료(§4 Phase 2 참조, 2026-07-03), **crontab 자동 등록은 미완료**라 항목 전체는 미체크 유지(Phase 7 `SYS_DB_BACKUP` 배치 작업에서 마무리 예정)
- [ ] 복구 테스트 완료 (백업 파일 → 신규 DB 복구 확인) — 미실시
- [ ] 외부 DB 클라이언트 접속 확인 (DBeaver 등, `localhost:5442`) — 미실시. 참고: 2026-07-03 보안 조치로 `db` 포트가 `127.0.0.1:5442`(호스트 로컬)로만 바인딩되어 있어, "외부"(원격 클라이언트) 접속은 설계상 불가하고 호스트 서버 로컬에서의 DBeaver 등 접속 여부만 확인 가능 — 항목 취지 재확인 필요

---

### 백엔드 `→ Phase 3`

- [x] FastAPI 프로젝트 구조 생성 (`app/core/`, `app/models/`, `app/schemas/`, `app/api/v1/`, `app/services/`) — 라우터 등록 구조(`api/v1/router.py`) 포함 완료, 2026-07-03
- [x] SQLAlchemy 2.x ORM 모델 작성 (16개 테이블 전체) — 16/16 완료, 실 서버 DB 적용 검증 완료 (2026-07-03)
- [x] Pydantic v2 스키마 작성 — 16개 테이블 전체 조회(Out) 스키마 작성 완료, 실 서버 컨테이너에서 실제 임포트 및 ORM 데이터 검증 완료 (2026-07-03)
- [x] `/health` 헬스체크 엔드포인트 구현
- [x] JWT 인증 API 구현 (`SYS_USER_MST` 기반 — 로그인, 토큰 갱신, 로그아웃) — 실 서버 HTTP 응답 확인 완료 (2026-07-03), 로그아웃 서버 측 즉시 무효화는 RBAC 미들웨어 도입 시 별도 처리 예정
- [x] CORS 설정 적용 (포트 3030 허용)
- [x] RBAC 권한 미들웨어 구현 (`SYS_ROLE_MST` 6개 역할) — 인증/권한 검사 의존성 구현 및 6개 라우터(`employees`/`skills`/`employee-skills`/`projects`/`assignments`/`codes`) 전체 적용 완료, `codes` 공통 권한 키 신규 추가 및 실 서버 검증 완료 (2026-07-03)
- [x] `SYS_AUDIT_LOG` 감사 로그 미들웨어 구현 — 로그인 및 5개 라우터의 등록/수정 행위 기록 구현, 실 서버 검증 완료 (2026-07-03). 조회(GET) 감사 로그 열람 API는 미구현
- [x] 사원 CRUD API (`HR_EMPL_MST` — `JIKMU_ID` 필드 포함) — 조회/등록/수정/퇴직 처리(`DELETE`, `EMPL_STAT_CD='RETIRED'` 전환) 구현, 실 서버 HTTP 응답 확인 완료 (2026-07-03)
- [ ] 직무 유형 CRUD API (`HR_JIKMU_MST`) — 조회만 구현(`GET /api/v1/job-types`, 2026-07-03), 등록/수정 미구현
- [x] 기술 CRUD API (`HR_SKILL_MST`, `HR_EMPL_SKILL_REL`) — 조회/등록/수정 구현(`GET`/`POST`/`PATCH /api/v1/skills`, `/api/v1/employee-skills`), 실 서버 HTTP 응답 확인 완료 (2026-07-03)
- [x] 부서/직급 코드 API (`HR_DEPT_MST`, `HR_JIKGUP_MST`) — 조회 API 구현 완료(`GET /api/v1/departments`, `/positions`), 실 서버 HTTP 응답 확인 완료 (2026-07-03)
- [x] 프로젝트 CRUD API (`PJT_MST`) — 조회/등록/수정 구현(`GET`/`POST`/`PATCH /api/v1/projects`), 실 서버 HTTP 응답 확인 완료 (2026-07-03)
- [x] 투입 관리 API (`PJT_ASGN_HIS`) — 조회/등록/수정 및 ALLOC_RT 100% 초과 검증 구현, 실 서버 HTTP 응답 확인 완료 (2026-07-03)
- [x] 가동률 계산 API (`HR_AVAIL_SNAP`) — `GET /api/v1/availability/{empl_id}` 즉시 계산 API 구현, 실 서버 검증 완료 (2026-07-03). 스냅샷 저장·배치 자동화는 Phase 7 `HR_AVAIL_SNAP_GEN` 몫으로 별도 유지
- [ ] 리소스 검색/추천 API (`PJT_RSRC_REQ`, `PJT_RCMD_RSLT`)
- [x] 대시보드 집계 API (직무 유형별 분포 포함) — SCR-002 설계서 명시 4개 엔드포인트 및 프론트엔드 목데이터(`lib/mock-data.ts`) 기반 4개 엔드포인트(데이터 품질, 이달 종료 예정, 최근 입사자, 월별 인력 추이) 총 8개 전부 구현, 실 서버 검증 완료 (2026-07-03)
- [x] Excel Import/Export API — Export(`GET /api/v1/employees/export`) + Import(`POST /api/v1/employees/import`) 전부 구현, 실 서버 검증 완료 (2026-07-03). Import 정책(마스터 미존재 시 전체 실패/`EMPL_NO` Upsert/부분 실패 시 전체 롤백)은 사용자 확정 사항 반영
- [x] 페이지네이션 공통 처리 구현 — `PaginationParams`/`PaginatedResponse` 공통 모듈로 추출, 3개 라우터 적용 및 실 서버 검증 완료 (2026-07-03)
- [x] OpenAPI 문서 확인 (`http://{서버IP}:8000/docs`) — 실 서버 `/docs`·`/redoc`·`/openapi.json` 정상 확인, 22개 엔드포인트 전부 등록 확인 (2026-07-03)

---

### 프론트엔드 `→ Phase 4`

- [x] Next.js 프로젝트 생성 (`output: 'standalone'` 설정 필수)
- [x] `NEXT_PUBLIC_API_BASE_URL` 환경변수 설정 (`http://{서버IP}:8000`)
- [x] 로그인 화면 구현 (`/login`) — MVP 임시 인증(`frontend/lib/auth.ts`), JWT API 연동 전까지 대체
- [x] 로그인 JWT API 연동 (`frontend/lib/auth.ts`의 localStorage 임시 마커를 `POST /api/v1/auth/login`·`/logout` 실제 호출로 교체) — 실 서버 컨테이너 빌드 및 번들 검증 완료 (2026-07-03). 토큰 저장은 MVP로 localStorage 유지
- [x] 공통 레이아웃·네비게이션 구현 (권한별 메뉴 제어) — 레이아웃/네비게이션/미인증 리다이렉트 및 `PERM_JSON` 기반 메뉴 필터링 전부 구현, 실 서버 검증 완료 (2026-07-03)
- [x] 대시보드 구현 (`/dashboard` — 직무 유형 분포 위젯 포함) — 목데이터를 백엔드 8개 API로 전량 교체, 실 서버 빌드·번들 검증 완료 (2026-07-03)
- [x] 사원 관리 화면 구현 (`/employees` — `JIKMU_ID` 필드·직무 유형 필터 포함) — 목데이터 기반, 실 API(`GET /api/v1/employees`) 연동 미완료
- [x] 사원 상세 화면 구현 (`/employees/[id]`) — 목데이터 스캐폴딩을 백엔드 실 API로 연동(기본정보/보유기술/투입이력), `GET /api/v1/employees/{empl_id}` 신규 추가, 실 서버 검증 완료 (2026-07-03). 정보수정/기술추가/퇴직처리는 조회 전용으로 남겨 후속 과제로 분리
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
| 2026-07-03 | v1.5 | §8 다음 작업 7번(사원 목록 조회 API) 완료 처리 — `backend/app/db/session.py`(DB 세션 의존성), `backend/app/schemas/hr_empl_mst.py`, `backend/app/repositories/hr_empl_mst.py`, `backend/app/api/v1/employees.py`, `backend/app/api/v1/router.py` 신규 작성, `backend/app/main.py`에 `/api/v1` 라우터 등록. Phase 3 상태를 "예정→진행 중"(0%→15%)으로 갱신 — 이미 완료돼 있던 FastAPI 기본 구조/`/health`/CORS를 반영. §5 기능별 구현 상태 "직원 관리" 행을 "진행 중(목록 조회만)"으로 갱신, §11 백엔드 체크리스트 3개 항목 완료 체크(FastAPI 구조, `/health`, CORS) 및 사원 CRUD API 부분 완료 명시. 실 서버 기동 기반 엔드포인트 호출 검증은 로컬 환경 제약(`fastapi`/`sqlalchemy` 미설치)으로 미실시 | — |
| 2026-07-03 | v1.6 | §8 다음 작업 8번(사원 등록/수정 API) 완료 처리 — `EmployeeCreate`/`EmployeeUpdate` 스키마, `create_employee`/`update_employee`/`get_employee` 리포지토리 함수, `POST`/`PATCH /api/v1/employees` 라우터 추가(UNIQUE/FK 위반 시 409 반환). §4/§5/§11의 "사원 CRUD API" 관련 서술을 "조회/등록/수정 구현, 퇴직 처리 미구현"으로 갱신(Phase 3 진행률은 보수적으로 15% 유지 — 완전한 CRUD 미완성). 실 서버 기동 기반 엔드포인트 호출 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v1.7 | §8 다음 작업 9번(Next.js 기본 레이아웃 구성) 완료 처리 — 기존 로그인/레이아웃/사이드바/상단바 스캐폴딩을 `frontend/lib/auth.ts`(신규, JWT API 전까지 임시 세션 마커)로 실제 동작하는 흐름으로 연결(로그인 시 세션 저장, 미인증 시 `/login` 리다이렉트, 로그아웃 시 세션 제거). Phase 4를 "예정→진행 중"(0%→20%)으로 갱신 — Phase 1에서 이미 완료돼 있던 `output: 'standalone'`/`NEXT_PUBLIC_API_BASE_URL`도 반영. §11 프론트엔드 체크리스트 3개 항목 완료 체크, "공통 레이아웃·네비게이션"은 권한별 메뉴 제어 미구현으로 부분 완료 유지. Next.js 빌드/타입체크는 로컬 환경 제약(Node 16, `node_modules` 미설치)으로 미실시 | — |
| 2026-07-03 | v1.8 | §8 다음 작업 10번(사원 목록 화면, 직무 유형 필터) 완료 처리 — `frontend/app/(app)/employees/page.tsx`의 기존 "보유 역할"(하드코딩 목록) 필터를 `HR_JIKMU_MST` 마스터 기반 `jobTypeOptions`("직무 유형")로 교체, 신규/구 코드 혼재 대응 별칭 매핑 추가. Phase 4 진행률 20%→25%로 갱신. §4/§11의 사원 목록 화면 항목 완료 체크(목데이터 기반, 실 API 미연동 명시). Next.js 빌드/타입체크는 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v1.9 | 실 서버 배포 검증 완료 및 버그 수정 5건 반영 — (1) `frontend/package.json`에 `packageManager` 고정(pnpm 11로 인한 lockfile 충돌 해결), (2) `frontend/public/.gitkeep` 추가(Docker 빌드 COPY 실패 해결), (3) `backend/alembic/env.py`의 `%` 이스케이프 처리(ConfigParser 보간 오류 해결, DATABASE_URL percent-encoding 대응), (4) `backend/app/models/{hr_empl_mst,pjt_mst,pjt_asgn_his}.py` 및 `alembic/versions/28ce52377e32_...py`의 CHECK 제약 6곳에 컬럼명 큰따옴표 추가(Postgres 대소문자 접힘으로 인한 "column does not exist" 오류 해결). 실 서버에서 Docker Compose v2(v5.2.0)·UFW(22/3030/8000)·`alembic upgrade head`(10개 테이블 생성+`SYS_ROLE_MST` 6종 Seed) 전부 정상 동작 확인. §3/§4 Phase 1 진행률 60%→75%로 갱신, §8 4~6번 및 §11 데이터베이스/인프라 체크리스트의 "미검증" 표기를 실 서버 확인 완료로 전환, §9에 `POSTGRES_PASSWORD` 노출 이력(로테이션 필요)·UFW 5442 제한 미확인 리스크 2건 추가 | — |
| 2026-07-03 | v2.0 | Phase 1 완료(100%) 처리 — `/health`·포트 3030 curl 응답 정상 확인. `docker-compose.yml`의 `db` 포트 바인딩을 `"5442:5432"` → `"127.0.0.1:5442:5432"`로 변경(UFW 대신 Docker 포트 바인딩 레벨에서 PostgreSQL 외부 노출 차단). `POSTGRES_PASSWORD` 로테이션 완료 확인. §9 리스크 2건(비밀번호 노출, UFW 5442) "해소" 처리, §3/§4 Phase 1을 "완료"로 갱신 | — |
| 2026-07-03 | v2.1 | `HR_EMPL_SKILL_REL` 테이블(ERD §3.6) 모델·마이그레이션 신규 작성 — §8 명시 항목 완료 이후 §3/§4 로드맵 순서상 가장 앞선 미완료 Phase(Phase 2)의 다음 순서로 진행. Phase 2 진행률 60%→65%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v2.2 | `HR_EMPL_ROLE_REL` 테이블(ERD §3.6-1) 모델·마이그레이션 신규 작성 — 복합 UNIQUE(`EMPL_ID`,`JIKMU_ID`) 제약 포함, `IS_PRIMARY` 정합성 규칙은 서비스 레이어 구현 대상으로 주석 명시. Phase 2 진행률 65%→70%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v2.3 | §8 다음 작업 섹션을 Phase 2 잔여 작업 중심 새 큐(0~10번)로 개편, 이미 완료된 항목 0·1은 근거와 함께 완료 처리. `HR_AVAIL_SNAP` 테이블(ERD §3.7) 모델·마이그레이션 신규 작성(`AVAIL_STAT_CD` CHECK 포함, 산정 배치는 Phase 7 별도 구현 예정). Phase 2 진행률 70%→75%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v2.4 | §8 다음 작업을 Rolling Backlog(누적 완료 목록이 아닌 다음 작업 큐) 원칙으로 재설정 — 완료된 `HR_EMPL_ROLE_REL`/`HR_AVAIL_SNAP` 항목은 목록에서 제외하고 §7/§11 근거만 남김. Phase 1 마무리 항목은 이미 완료된 사실이 있으나 요청에 따라 0번으로 유지하고 완료 상태로 정확히 표기. 잔여 작업을 `PJT_RSRC_REQ`→`PJT_RCMD_RSLT`→`SYS_BATCH_HIS`→Seed→마이그레이션 체인 점검→실 서버 적용 검증→Phase 2 완료 기준 점검 순으로 재구성 | — |
| 2026-07-03 | v2.5 | `PJT_RSRC_REQ` 테이블(ERD §3.10) 모델·마이그레이션 신규 작성 — Rolling Backlog 원칙에 따라 §8에서 완료 항목 제거 및 나머지 재번호(1~6). Phase 2 진행률 75%→80%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v2.6 | `PJT_RCMD_RSLT` 테이블(ERD §3.11) 모델·마이그레이션 신규 작성 — §8에서 완료 항목 제거 및 나머지 재번호(1~5). Phase 2 진행률 80%→85%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v2.7 | `SYS_BATCH_HIS` 테이블(ERD §3.15) 모델·마이그레이션 신규 작성 — ERD 16개 테이블 전체 모델·마이그레이션 작성 완료. 8개 Alembic 리비전이 분기 없는 단일 선형 체인임을 전수 대조로 확인(체인 점검 항목 겸 완료). Phase 2 진행률 85%→90%로 갱신, §8 큐를 Seed/실 서버 검증/Phase2 완료 점검 3개 항목으로 재정리 | — |
| 2026-07-03 | v2.8 | `HR_JIKGUP_MST`(10종)/`HR_JIKMU_MST`(12종) Seed 데이터 신규 작성 및 Alembic 리비전(`370c95546556`, head 뒤 체이닝)으로 반영 — 로드맵 §11 Seed 항목 3종(`SYS_ROLE_MST`/`HR_JIKGUP_MST`/`HR_JIKMU_MST`) 전부 완료. Phase 2 진행률 90%→95%로 갱신, §8 큐를 실 서버 검증/Phase2 완료 점검 2개 항목으로 재정리 | — |
| 2026-07-03 | v2.9 | **Phase 2 100% 완료** — 실 서버에서 `alembic upgrade head`(7개 리비전 적용), 16개 테이블 생성(`\dt`), Seed 3종 삽입(`SELECT COUNT(*)`), `pg_dump` 백업 파일 생성을 전부 실측 검증 완료. §4/§11의 "실 DB 미검증" 표기 전량을 "실 서버 DB 적용 검증 완료"로 갱신, Phase 2 완료 기준 3개 항목 충족 처리. §8 다음 작업을 Phase 3(FastAPI 백엔드, 20%) 잔여 작업 11개 항목으로 전면 재구성 | — |
| 2026-07-03 | v3.0 | 16개 테이블 전체 Pydantic v2 조회(Out) 스키마 작성 완료 — 실 서버 컨테이너 내 실제 임포트 및 ORM 데이터(`PERM_JSON` JSONB, KST 타임존) 검증까지 수행(`novauser` 계정 `docker` 그룹 권한 확인 후 `sg docker`로 직접 접근). `SysUserOut`에서 `ENCR_PWD` 의도적 제외 확인. Phase 3 진행률 20%→28%로 갱신, §8 큐에서 완료 항목 제거 및 재번호(1~9) | — |
| 2026-07-03 | v3.1 | 부서/직급/직무 코드 조회 API 구현 — `GET /api/v1/departments`·`/positions`·`/job-types` 신규 라우터·리포지토리 추가, 실 서버에서 `curl`로 실제 응답(10건/12건) 및 `openapi.json` 경로 등록 확인. Phase 3 진행률 28%→33%로 갱신, §11 "부서/직급 코드 API" 완료 체크, "직무 유형 CRUD API"는 조회만 완료로 갱신 | — |
| 2026-07-03 | v3.2 | §8 다음 작업 1번(기술 CRUD API) 완료 처리 — `SkillCreate`/`SkillUpdate`, `EmployeeSkillCreate`/`EmployeeSkillUpdate` 스키마 및 리포지토리·라우터(`app/api/v1/skills.py`, `app/api/v1/employee_skills.py`) 신규 작성, `employees.py` 패턴 재사용. 실 서버 재빌드 후 `curl`로 등록/조회/수정 및 422(범위 밖 `PRFCY_LEVL`)/409(FK 위반) 응답 확인. Phase 3 진행률 33%→39%로 갱신, §11 "기술 CRUD API" 완료 체크, §8 큐에서 제거 및 재번호(1~8) | — |
| 2026-07-03 | v3.3 | §8 다음 작업 1번(프로젝트 CRUD API) 완료 처리 — `ProjectCreate`/`ProjectUpdate`/`ProjectListResponse` 스키마(`PJT_STAT_CD`는 `PJT_STAT_CODES` 상수 기반 `Literal` 검증) 및 리포지토리·라우터(`app/repositories/pjt_mst.py`, `app/api/v1/projects.py`) 신규 작성, `employees.py`의 skip/limit 페이지네이션 패턴 재사용. 실 서버 재빌드 후 `curl`로 등록/조회/수정, 409(`PJT_CD` 중복), 422(잘못된 상태값), 404(존재하지 않는 ID) 응답 전부 확인. Phase 3 진행률 39%→44%로 갱신, §11 "프로젝트 CRUD API" 완료 체크, §8 큐에서 제거 및 재번호(1~7) | — |
| 2026-07-03 | v3.4 | §8 다음 작업 1번(투입 관리 API) 완료 처리 — `AssignmentCreate`/`AssignmentUpdate`/`AssignmentListResponse` 스키마 및 리포지토리·라우터(`app/repositories/pjt_asgn_his.py`, `app/api/v1/assignments.py`) 신규 작성. ERD §3.9/설계서 §5.5의 "동일 사원 동일 기간 ALLOC_RT 합계 100% 초과 금지" 규칙을 `sum_overlapping_alloc_rt` 헬퍼로 구현해 등록/수정 시 409로 거부하도록 적용(집계 대상 상태 MVP 해석은 §9 리스크로 별도 기록). 실 서버 재빌드 후 임시 테스트 데이터로 100%/초과/취소 제외/404 케이스 전부 확인 후 테스트 데이터 삭제. Phase 3 진행률 44%→50%로 갱신, §11 "투입 관리 API" 완료 체크, §9 리스크 1건 추가, §8 큐에서 제거 및 재번호(1~6) | — |
| 2026-07-03 | v3.5 | §8 다음 작업 1번(JWT 인증 API) 완료 처리 — `backend/app/core/security.py`(비밀번호 해싱, JWT 발급/검증), `backend/app/schemas/auth.py`, `backend/app/repositories/sys_user_mst.py`, `backend/app/api/v1/auth.py`(`POST /api/v1/auth/{login,refresh,logout}`) 신규 작성. 실 서버 재빌드 중 `passlib[bcrypt]==1.7.4`/`bcrypt>=4.1` 비호환 버그 발견해 `backend/requirements.txt`에 `bcrypt==4.0.1` 고정으로 해결(§9 리스크 기록). 임시 역할·사용자 데이터로 로그인/토큰 갱신/로그아웃 및 401 경로 전부 확인 후 삭제. `.env`의 `JWT_SECRET_KEY`는 이미 설정되어 있어 별도 수정 불필요. Phase 3 진행률 50%→56%로 갱신, §11 "JWT 인증 API" 완료 체크, §9 리스크 2건 추가(로그아웃 무효화 미구현, bcrypt 호환성), §8 큐에서 제거 및 재번호(1~5) | — |
| 2026-07-03 | v3.6 | §8 다음 작업 1번(RBAC 권한 미들웨어) 부분 완료 — `backend/app/api/deps.py`(신규, `get_current_user`/`require_permission`) 작성 및 `PERM_JSON` 화면 키가 명확한 5개 라우터(`employees`/`skills`/`employee_skills`/`projects`/`assignments`)에 적용. `codes.py`는 대응 화면 키(`departments`/`positions`) 부재로 적용 보류(§9 리스크 추가) — 항목은 "진행 중"으로 유지, §8 큐에서 제거하지 않음. 실 서버에서 VIEWER/PM 역할 테스트 사용자로 401/403/200/201 경로가 `PERMISSION_MATRIX.md`와 일치함을 확인. Phase 3 진행률은 보수적으로 56% 유지, §11 해당 항목 "진행 중"으로 갱신 | — |
| 2026-07-03 | v3.7 | **체크리스트/상태표 정합성 점검(사용자 요청)** — 실 서버 재확인 결과 §11 데이터베이스 체크리스트의 "PostgreSQL Docker 컨테이너 구성"/"바인드 마운트 확인" 2개 항목이 실제로는 Phase 1 완료 시 이미 검증되었음에도 체크 표시가 누락되어 있어 `[x]`로 정정(`docker compose ps` 및 `data/postgres/pgdata` 실존 확인). "Seed 데이터 입력" 항목의 "실 DB 적용 미검증" 문구가 Phase 2 100% 완료 검증(2026-07-03) 이후 갱신되지 않은 것도 발견해 정정. "DB 백업 스크립트+crontab" 항목은 스크립트 작성/수동 실행만 완료(crontab 미완료)임을 명확히 하는 설명을 추가했으나 체크는 보류. "외부 DB 클라이언트 접속 확인" 항목에는 5442 포트가 `127.0.0.1`로만 바인딩되어 있어 문자 그대로의 "외부" 접속은 설계상 불가하다는 점을 주석으로 추가(체크는 보류). 추가로 §5 "기능별 구현 상태"·§6 "기술 구성 요소별 진행 상태" 두 표가 최초 작성 이후 한 번도 갱신되지 않아 이미 완료된 다수 항목(Docker/PostgreSQL/FastAPI/SQLAlchemy/Alembic 등 인프라 전체, 기술/직원기술/프로젝트/투입관리/투입률검증/배포자동화 등 API 기능)이 "예정"으로 남아있던 것을 확인해 실제 상태(완료/진행 중/예정)로 전면 갱신. §3 전체 로드맵 표의 Phase 3 진행률이 33%로 정체되어 있던 것을 §4 상세표 기준 56%로 정정. 실질적인 기능/코드 변경은 없음(문서 정합성 정정만 수행) | — |
| 2026-07-03 | v3.8 | §8 다음 작업 2번(`SYS_AUDIT_LOG` 감사 로그 미들웨어) 완료 처리 — `backend/app/repositories/sys_audit_log.py`, `backend/app/core/audit.py`(`record_audit`) 신규 작성. 로그인 및 `employees`/`skills`/`employee_skills`/`projects`/`assignments` 5개 라우터의 등록/수정 엔드포인트에 적용(도메인별 Out 스키마로 변경 전/후 스냅샷 기록). `codes.py`는 RBAC 미적용과 동일하게 제외(§9 참조). 실 서버에서 ADMIN 테스트 사용자로 로그인→등록→수정을 실행해 `SYS_AUDIT_LOG`에 `LOGIN`/`CREATE`/`UPDATE` 3건이 정확히 기록됨을 확인(BFR/AFT JSON 값 일치 포함). Phase 3 진행률 56%→61%로 갱신, §11 "SYS_AUDIT_LOG 감사 로그 미들웨어" 완료 체크, §8 큐에서 제거 및 재번호(1~4) | — |
| 2026-07-03 | v3.9 | **RBAC 잔여 범위 완료 — `codes` 공통 코드 권한 신설(운영팀 확인 반영)** — 부서(`departments`)/직급(`positions`)을 독립 화면이 아닌 "공통 코드/기준정보"로 취급하기로 확정(운영팀 확인). `SYS_ROLE_MST.PERM_JSON`에 `codes` 키 신설(`codes.view` 전 역할 허용, `codes.create/update/delete`는 ADMIN/HR_MGR만 허용) — `sys_role_mst_seed.py` Seed 소스 갱신 및 Alembic 리비전 `9c1f3a5d2b7e`(head `370c95546556` 뒤 체이닝, `jsonb_set`으로 기존 DB 행 갱신)로 실 DB 반영. `GET /api/v1/job-types` 조회에도 `codes.view` 정책 병행 적용(관리 화면 등록/수정/삭제는 기존 `job_types.*` A H 전용 유지). `backend/app/api/v1/codes.py` 3개 GET 엔드포인트에 `require_permission("codes", "view")` 적용 — 인증 없이 호출 가능하던 마지막 업무 API 제거. `backend/docs/PERMISSION_MATRIX.md`에 `codes` 권한 섹션 및 화면 키 목록(14종) 갱신. 실 서버에서 `alembic upgrade head` 적용 후 6개 역할 `PERM_JSON` 값 확인, 인증 없이 코드 API 호출 시 401 전환 확인, VIEWER 테스트 사용자로 3개 엔드포인트 정상 조회(200) 확인. Phase 3 진행률 61%→67%로 갱신, §11 "RBAC 권한 미들웨어 구현" 진행 중→완료로 정정, §9 리스크 "departments/positions/job-types 화면 권한 키 미정" 주의→해소 처리(처리일자 2026-07-03) | — |
| 2026-07-03 | v4.0 | §8 다음 작업 1번(사원 퇴직 처리 API) 완료 처리 — `backend/app/repositories/hr_empl_mst.py`에 `retire_employee`(신규, `EMPL_STAT_CD='RETIRED'` 전환 + `RETIR_DT` 기록) 추가, `backend/app/api/v1/employees.py`에 `DELETE /api/v1/employees/{empl_id}` 라우터 추가(`retir_dt` 쿼리 파라미터 지원, 기존 `employees.delete` 권한·감사 로그 재사용). 실 서버에서 임시 사원 데이터로 정상 퇴직 전환, 재퇴직 시도 409, 미존재 404, 무인증 401, 권한 없는 역할 403, `SYS_AUDIT_LOG`에 `ACT_CD='DELETE'`(변경 전/후 상태 포함) 기록까지 전부 확인 후 테스트 데이터 삭제. Phase 3 진행률 67%→72%로 갱신, §5·§11 "사원 CRUD API"/"직원 관리" 완료 체크로 정정, §8 큐에서 완료 항목 제거 및 재번호(1~2) | — |
| 2026-07-03 | v4.1 | §8 다음 작업 1번(페이지네이션 공통 처리) 완료 처리 — `backend/app/core/pagination.py`(`PaginationParams`), `backend/app/schemas/pagination.py`(`PaginatedResponse[T]` 제네릭) 신규 작성. `EmployeeListResponse`/`ProjectListResponse`/`AssignmentListResponse`를 제네릭 타입 별칭으로 전환(응답 JSON 형태 동일 유지), `employees`/`projects`/`assignments` 3개 라우터의 개별 skip/limit `Query` 선언을 `Depends(PaginationParams)`로 교체. 실 서버 재빌드 후 기본값/커스텀 값/422 검증 범위가 기존과 동일하게 동작함을 확인. `/openapi.json` 스키마명이 `PaginatedResponse_XOut_` 형태로 바뀌는 부수 효과를 §9 리스크로 기록(응답 바디 무영향). Phase 3 진행률 72%→78%로 갱신, §11 "페이지네이션 공통 처리 구현" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1) | — |
| 2026-07-03 | v4.2 | §8 다음 작업 1번(OpenAPI 문서 확인) 완료 처리 — 코드 변경 없이 실 서버에서 `/docs`·`/redoc`·`/openapi.json` 정상 응답 및 22개 엔드포인트 태그·설명·응답 코드·`HTTPBearer` 보안 스키마 반영을 확인. Phase 3 진행률 78%→83%로 갱신, §11 "OpenAPI 문서 확인" 완료 체크, §8 큐를 §4 Phase 3 미착수 항목(가동률 계산 API, 대시보드 집계 API, Excel Import/Export API) 3개로 재구성 | — |
| 2026-07-03 | v4.3 | §8 다음 작업 1번(가동률 계산 API) 완료 처리 — `backend/app/repositories/hr_avail_snap.py`(`compute_availability`, `AVAILABILITY_CALC_SPEC.md` §2/§4 로직 구현), `backend/app/schemas/hr_avail_snap.py`(`AvailabilityCalcOut`), `backend/app/api/v1/availability.py`(신규, `GET /api/v1/availability/{empl_id}`) 작성. `HR_AVAIL_SNAP` 테이블에 저장하지 않는 즉시 계산 전용 API로 설계(스냅샷 생성 배치는 Phase 7 `HR_AVAIL_SNAP_GEN` 몫으로 이미 문서화되어 있어 중복 구현 회피). 실 서버에서 AVAILABLE/PARTIAL/FULL(종료일 있음)/FULL(데이터 품질 경고)/PROPOSED 제외 5가지 케이스 및 404/401 전부 확인 후 테스트 데이터 삭제. Phase 3 진행률 83%→89%로 갱신, §5 "가동 가능일 자동 계산" 예정→진행 중, §11 "가동률 계산 API" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1~2) | — |
| 2026-07-03 | v4.4 | §8 다음 작업 1번(대시보드 집계 API) 완료 처리 — SCR-002 설계서 명시 4개 엔드포인트(`summary`/`dept-utilization`/`job-type-distribution`/`utilization-by-type`) 신규 구현(`app/repositories/dashboard.py`, `app/schemas/dashboard.py`, `app/api/v1/dashboard.py`). `hr_avail_snap.py`에 `active_alloc_rt_subquery` 추출해 가동률 계산 로직 재사용. `HR_AVAIL_SNAP` 배치 미구현으로 실시간 재계산 방식 채택(§9 리스크 기록). 실 서버에서 부서 2개·사원 3명 임시 데이터로 4개 엔드포인트 결과를 수기 계산과 대조해 전부 일치 확인. Phase 3 진행률 89%→94%로 갱신, §11 "대시보드 집계 API" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1, Excel Import/Export API만 남음) | — |
| 2026-07-03 | v4.5 | 사용자 요청으로 프론트엔드 `/dashboard` 목데이터(`lib/mock-data.ts`) 기준 미구현 위젯 4개 API 추가 — `GET /api/v1/dashboard/{data-quality,ending-this-month,recent-employees,headcount-trend}`. 기존 SCR-002 설계서 명시분(4개)과 합쳐 대시보드 API 총 8개 완성. 임시 사원 3명 데이터로 데이터 품질(기술/직무 미등록, 100% 초과)·이달 종료 예정 상세·최근 입사자(퇴직자 제외)·3개월 인력 추이(입사/퇴사 반영)를 수기 계산과 대조해 전부 검증 완료. §11 "대시보드 집계 API" 항목 설명을 8개 엔드포인트 기준으로 갱신 | — |
| 2026-07-03 | v4.6 | 사용자 요청으로 프론트엔드 전체 한글 폰트를 Noto Sans KR로 변경 — `frontend/app/layout.tsx`에서 `Geist`(라틴 전용)를 `Noto_Sans_KR`(subsets `latin`+`korean`)로 교체, `--font-geist-sans` CSS 변수명은 유지해 영향 범위 최소화. `globals.css` 폴백 폰트명 갱신. `docker compose up -d --build web` 재빌드로 TypeScript/Next.js 빌드 정상 통과 확인(로컬 Node 16 제약 대체 검증), 실 서버에서 `font-family: Noto Sans KR` 적용 및 `/login` 정상 렌더링 확인 | — |
| 2026-07-03 | v4.7 | §8 다음 작업 1번(Excel Import/Export API) 중 Export만 완료 처리 — SCR-003 컬럼 매핑 그대로 `GET /api/v1/employees/export`(`openpyxl` 신규 의존성) 구현, 보유역할·주요기술·숙련도 N:M 집계 헬퍼 추가. Import는 FK 명칭 조회·upsert·부분 실패 정책 등 설계 판단이 필요해 별도 항목으로 분리(§9 리스크 기록). 실 서버에서 `.xlsx` 실제 내용 검증(10개 컬럼 전부 정확), `excel` 권한 없는 역할 403, 무인증 401, `SYS_AUDIT_LOG` EXPORT 기록 확인. §11 "Excel Import/Export API" 항목을 Export 완료·Import 미구현으로 설명 갱신(체크박스 미완료 유지), §8 큐를 Import 전용 항목으로 재구성 | — |
| 2026-07-03 | v4.8 | 사용자 요청으로 백로그 문서에 누락되어 있던 "로그인 JWT API 연동" 항목 신규 추가 — 백엔드 JWT 인증 API는 완료되었으나 프론트엔드가 `lib/auth.ts`의 localStorage 임시 마커 대신 실제 API를 호출하도록 연동하는 작업 자체를 가리키는 백로그 항목이 없었음을 확인해 추가. §4 Phase 4 "주요 작업" 표·§11 프론트엔드 체크리스트에 신규 항목(예정) 추가, §8 다음 작업 큐에 2번 항목으로 등록. 코드 변경 없음(문서 정정만 수행) | — |
| 2026-07-03 | v4.9 | §8 다음 작업 2번(로그인 JWT API 연동) 완료 처리 — `frontend/lib/auth.ts`를 localStorage 세션 마커 방식에서 실제 액세스/리프레시 토큰 저장 방식으로 교체(`login`/`logout`/`getAccessToken` 신규, `isAuthenticated` 시그니처 유지). `login/page.tsx`의 목업 로직을 실제 `POST /api/v1/auth/login` 호출로, `top-nav.tsx`의 로그아웃을 실제 `POST /api/v1/auth/logout` 호출로 교체. 토큰 저장은 MVP로 localStorage 유지(HttpOnly Cookie 전환은 백엔드 API 변경 필요해 별도 후속 과제, §9 리스크 기록). 실 서버 컨테이너 재빌드로 TypeScript/Next.js 빌드 통과 확인, 컴파일된 번들에서 `USER_LGID` 로그인 페이로드 실존 확인(브라우저 클릭 테스트는 headless 도구 부재로 미실시). Phase 4 진행률 25%→31%로 갱신, §4/§6/§11 관련 항목 갱신, §9 리스크 1건 추가, §8 큐에서 완료 항목 제거(Excel Import만 남음) | — |
| 2026-07-03 | v5.0 | Excel Import 정책 확정 반영: 마스터 미존재 시 전체 실패, `EMPL_NO` 기준 Upsert, 일부 실패 시 전체 롤백 (사용자 확정) — `POST /api/v1/employees/import` 신규 구현(`backend/app/services/employee_import.py`: 파싱·검증·Upsert·역할/기술 동기화, `python-multipart` 신규 의존성). 실 서버에서 정상/마스터 미존재/파일 내 사번 중복/기존 사번 수정 4개 시나리오 및 권한/인증/감사 로그 전부 검증 완료, 실패 시나리오는 DB 무변경 확인. §4 "Excel Import/Export API" 완료 처리, §11 항목 완료 체크. **Phase 3 재점검**: 주요 작업 전 항목 완료로 진행률 100% 갱신했으나, "완료 기준"의 "Pytest 단위 테스트 핵심 API 커버"가 미충족임을 확인해 Phase 3을 "완료"로 선언하지 않음 — §8 다음 작업을 "Pytest 단위 테스트 스위트 구축"으로 재구성, §9 리스크 1건 추가 | — |
| 2026-07-03 | v5.1 | **버그 수정** — `NEXT_PUBLIC_API_BASE_URL`이 프론트엔드 Docker 이미지 빌드 시점에 클라이언트 번들로 인라인되지 않던 문제 발견 및 수정(사용자가 프론트엔드 로그인 화면에서 로그인이 안 된다고 보고해 조사 중 발견). `docker-compose.yml`의 `web.build`에 `args: {NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL}}` 추가, `frontend/Dockerfile` builder 스테이지에 `ARG`/`ENV` 선언 추가. Phase 1 때부터 잠재했던 버그로, 화면이 목데이터만 쓰던 동안은 드러나지 않다가 로그인 JWT 연동(v4.9) 이후 처음 실제 영향이 나타남 — 재빌드 후 클라이언트 번들에 백엔드 URL이 정상 포함되고 CORS 프리플라이트·실제 로그인 요청이 브라우저와 동일한 조건(Origin 헤더 포함)으로 정상 동작함을 확인. `.env`/DESIGN 파일은 수정하지 않음. §9 리스크에 "해소"로 기록, §11 관련 항목 설명 갱신 | — |
| 2026-07-03 | v5.2 | **Phase 3(FastAPI 백엔드 구축) 정식 완료** — Pytest 단위 테스트 스위트 신규 구축(`backend/tests/`, 16개 테스트: health/인증/RBAC/사원 CRUD/투입관리 ALLOC_RT 검증). 실 DB 연결+SAVEPOINT 격리 패턴으로 테스트 후 자동 롤백되어 DB에 흔적을 남기지 않도록 구현, 실 서버 컨테이너에서 16개 전부 통과 및 잔여 데이터 0건 확인. §4 Phase 3 "완료 기준" 4개 항목 전부 충족되어 개발 상태 "완료"·진행률 100%로 전환, §3 전체 로드맵 갱신, §9 리스크 해소 처리, §8 큐를 Phase 4(Next.js) 잔여 항목으로 재구성 | — |
| 2026-07-03 | v5.3 | §8 다음 작업 1번(공통 레이아웃·네비게이션 권한별 메뉴 제어) 완료 처리 — `GET /api/v1/auth/me`(신규, `MeOut` 스키마) 추가해 프론트엔드가 현재 사용자의 `ROLE_CD`/`PERM_JSON`을 조회할 수 있게 함. `frontend/lib/nav.ts`에 `NavItem.permKey` 필드와 `filterNavByPermissions` 헬퍼 추가, `lib/auth.ts`에 `getMe()` 추가, `app-shell.tsx`가 로그인 확인 후 `getMe()` 호출 결과를 `Sidebar`(데스크톱/모바일 공통)에 전달해 메뉴를 화면 권한 기준으로 필터링. `backend/tests/test_auth.py`에 `/auth/me` 테스트 2건 추가(pytest 16→18개 전부 통과). 실 서버에서 `admin` 계정으로 `/auth/me` 정상 응답, 무인증 401, 프론트엔드 재빌드 후 번들에 호출 코드 포함 확인. Phase 4 진행률 31%→38%로 갱신, §4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거(대시보드 화면 구현만 남음) | — |
| 2026-07-03 | v5.4 | §8 다음 작업 1번(대시보드 화면 구현) 완료 처리 — `frontend/app/(app)/dashboard/page.tsx`를 목데이터에서 백엔드 대시보드 API 8종 실 호출로 전면 교체. `HeadcountChart`/`JobTypeDonut`/`DeptUtilizationChart` 3개 차트 컴포넌트를 `data` prop 기반으로 리팩터링(소비처인 `reports/page.tsx`도 호환 유지 위해 함께 수정), 인증 API 호출 공통 헬퍼 `frontend/lib/api.ts`(`apiGet<T>`) 신규 작성. 실 서버 재빌드 성공(`/dashboard` 정적 프리렌더, TypeScript 컴파일 오류 없음), 컴파일된 번들에 실 API 호출 코드 포함 확인, `admin` 토큰으로 8개 엔드포인트 전부 직접 호출해 응답 구조가 화면의 TypeScript 인터페이스와 일치함을 확인. Phase 4 진행률 38%→44%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐를 Phase 4 잔여 미완료 항목(사원 상세~설정 화면 등 9개)으로 재구성 | — |
| 2026-07-03 | v5.5 | §8 다음 작업 1번(사원 상세 화면 구현) 완료 처리 — 기존 저장소에 이미 있던 목데이터 기반 `/employees/[id]` 프로토타입 화면을 실 API로 연동(기본정보/보유기술/투입이력 3개 탭). 신규 `GET /api/v1/employees/{empl_id}` 백엔드 엔드포인트 추가(기존 `get_employee` 리포지토리 재사용), 기술·투입 이력 조회는 기존 API 그대로 재사용. 정보수정/기술추가/퇴직처리 UI와 "변경 이력" 탭(감사 로그 조회 API 부재)은 후속 작업으로 분리, §9 리스크 4건 추가(편집 UI 미구현·감사 로그 API 부재·부서 마스터 Seed 없음·`hrm-worker` 재시작 루프). `backend/tests/test_employees.py`에 상세 조회 테스트 3건 추가(pytest 18→21개 전부 통과). 실 서버에서 임시 부서·사원 데이터로 상세 조회 200/404, 응답 구조 일치 확인(검증 중 투입 이력 응답이 페이지네이션 래퍼임을 발견해 프론트엔드 파싱 버그 수정). Phase 4 진행률 44%→50%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐 재구성(누락되었던 "설정 화면 구현"·"Excel Import/Export UI 구현" 2개 항목도 함께 추가) | — |

