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
| Phase 4 | Next.js 웹 클라이언트 구축 | 3~5주차 | 완료 | 100% | 정상 |
| Phase 5 | 리소스 검색 및 추천 기능 구축 | 5주차 | 완료 | 100% | 정상 |
| Phase 6 | AI 질의응답 연동 | 7주차 | 완료 | 100% | 정상 |
| Phase 7 | 운영 자동화 및 배포 안정화 | 6~7주차 | 진행 중 | 20% | 정상 |
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
| **개발 상태** | 완료 |
| **진행률** | 100% |
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
| 사원 목록 화면 구현 (`/employees`) — 직무 유형 필터 포함 | 완료 (목데이터를 백엔드 실 API로 전량 교체 — `GET /api/v1/employees`+`departments`/`positions`/`job-types`/`employee-roles`(신규)/`availability` 병렬 조회 후 클라이언트 조인, 조직·직급·직무 유형 필터도 실 마스터 데이터 기준으로 동적 생성, 실 서버 검증 완료, 2026-07-04. "사원 등록" 모달은 여전히 UI 전용 스텁으로 남아 후속 과제로 분리 — §9-1 참조) |
| 사원 상세 화면 구현 (`/employees/[id]`) | 완료 (기존 목데이터 기반 스캐폴딩을 백엔드 실 API로 연동 — 기본정보/보유기술/투입이력 3개 탭 실 데이터 조회, 신규 `GET /api/v1/employees/{empl_id}` 추가, 실 서버 빌드·검증 완료, 2026-07-03. 정보수정/기술추가/퇴직처리 버튼은 조회 전용으로 남기고 후속 작업으로 분리 — §9 참조) |
| 기술 관리 화면 구현 (`/skills`) | 완료 (목데이터를 백엔드 실 API(조회/등록/수정/사용여부 토글)로 전량 교체, 실 서버 빌드·검증 완료, 2026-07-04) |
| 직무 유형 관리 화면 구현 (`/job-types`) | 완료 (목데이터를 백엔드 실 API로 전량 교체, `POST`/`PATCH /api/v1/job-types` 신규 추가, 실 서버 검증 완료, 2026-07-04) |
| 프로젝트 목록/상세 화면 구현 (`/projects`, `/projects/[id]`) | 완료 (목데이터를 백엔드 실 API로 전량 교체, `GET /api/v1/projects/{pjt_id}` 신규 추가, 실 서버 검증 완료, 2026-07-04. 수정/종료처리/인력투입 UI는 조회 전용으로 남겨 후속 과제로 분리) |
| 투입 관리 화면 구현 (`/assignments`) | 완료 (목데이터를 백엔드 실 API로 전량 교체, 등록 모달 신규 추가(기존 백엔드 API 재사용), 실 서버 검증 완료, 2026-07-04) |
| 가동 가능 인력 조회 화면 구현 (`/availability`) | 완료 (목데이터를 백엔드 실 API로 전량 교체, 일괄 조회 API `GET /api/v1/availability` 신규 추가, 직무 유형 필터 포함, 실 서버 검증 완료, 2026-07-04) |
| 리포트 화면 구현 (`/reports`) | 완료 (주간/월간/월별 가동률 통계 매트릭스 3개 탭 전부 실 API 연동, `GET /api/v1/reports/{weekly,monthly,utilization-matrix}` 신규 추가, 실 서버 검증 완료, 2026-07-04(매트릭스는 2026-07-04 추가 완료). 탭 순서를 사용자 요청으로 "매트릭스/주간/월간"으로 변경. 리포트 발송·가동률 통계 Excel 내보내기는 후속 과제로 분리) |
| 설정 화면 구현 (`/settings/users`, `/settings/audit-logs`) | 완료 (사용자 관리·감사 로그 조회를 백엔드 실 API로 전량 교체, `GET/POST /api/v1/users`, `GET /api/v1/users/roles`, `GET /api/v1/audit-logs` 신규 추가, 실 서버 검증 완료, 2026-07-04. 계정 수정/비활성화·감사 로그 Excel 내보내기는 후속 과제로 분리) |
| Excel Import/Export UI 구현 | 완료 (사원 목록 화면에 "Excel 가져오기/내보내기" 버튼 신규 추가, 기존 `GET/POST /api/v1/employees/{export,import}` API 연동, 실 서버 검증 완료, 2026-07-04. 검증 중 `GET /export`가 `GET /{empl_id}` UUID 경로 라우트에 등록 순서상 가로채여 항상 422를 반환하던 기존 버그를 발견해 함께 수정 — 회귀 방지 테스트 `backend/tests/test_employees_excel.py` 신규 추가. 사원 목록 화면 자체는 여전히 목데이터 기반이라 Import 성공 후에도 화면 목록은 갱신되지 않음 — 기존 §9-1 "사원 목록 화면 — 실 API 미연동" 항목과 동일 사안) |

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
| **개발 상태** | 완료 |
| **진행률** | 100% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| 가동 가능일 자동 계산 로직 구현 (`HR_AVAIL_SNAP` 기반, MVP 산정 기준 확정 — `backend/docs/AVAILABILITY_CALC_SPEC.md` 참조) | 완료 (매일 01:00 배치 `HR_AVAIL_SNAP_GEN`을 Phase 7에서 구현 완료(`app/services/avail_snap_gen.py`, `app/worker.py`) — `HR_AVAIL_SNAP` 테이블에 스냅샷 저장, 실 서버 검증 완료, 2026-07-04) |
| 즉시 투입 가능 인력 조회 API 구현 | 완료 (`GET /api/v1/availability`, 2026-07-04 "가동 가능 인력 조회 화면 구현" 작업에서 완료 — 이 표에 반영 누락되어 있던 것을 이번에 바로잡음) |
| 직무 유형·기술·숙련도 복합 필터 검색 API 구현 | 완료 (`GET /api/v1/availability`에 `skill_id`/`min_prfcy_levl` 쿼리 파라미터 신규 추가, 기존 직무 유형·부서 필터와 함께 복합 적용, 실 서버 검증 완료, 2026-07-04) |
| 추천 점수 산정 로직 구현 (직무 일치 15% + 기술 35% + 숙련도 25% + 가동일 15% + 유사경험 7% + 역할적합도 3%) | 완료 (`backend/app/repositories/pjt_rcmd_rslt.py`, 각 항목 산정 방식은 설계서에 세부 공식이 없어 MVP 해석 적용 — §9 리스크 참조, 2026-07-04) |
| `PJT_RSRC_REQ` 인력 요청 등록 API 구현 | 완료 (`POST /api/v1/resource-requests`, 실 서버 검증 완료, 2026-07-04) |
| `PJT_RCMD_RSLT` 추천 결과 저장 및 조회 API 구현 | 완료 (`POST /api/v1/recommendations/score`, `GET /api/v1/recommendations/{req_id}`, 실 서버 검증 완료, 2026-07-04) |
| 리소스 추천 화면 구현 (`/recommendations`) — 직무 유형 조건 포함 | 완료 (목데이터를 백엔드 실 API로 전량 교체, 실 서버 검증 완료, 2026-07-04) |
| 가동 가능 인력 화면 구현 (`/availability`) | 완료 (2026-07-04 완료 — 이 표에 반영 누락되어 있던 것을 이번에 바로잡음, §4 Phase 4 표·§7·§11 참조) |

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
| **개발 상태** | 완료 |
| **진행률** | 100% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| LLM 연동 인터페이스 추상화 (멀티 LLM 전환 가능 구조) | 완료 (`backend/app/services/ai_chat.py`의 `call_llm` — `LLM_PROVIDER` 설정값으로 공급자 분기, 현재 DeepSeek만 지원. `backend/app/core/config.py`에 `LLM_PROVIDER`/`DEEPSEEK_*` 필드 신규 추가, 실 서버에서 DeepSeek API 실제 인증 호출 검증 완료, 2026-07-04) |
| 자연어 조건 파싱 구현 (`JIKMU_CD`, `SKILL_NM`, 가동일 인식) | 완료 (`backend/app/services/ai_parser.py`(신규) — LLM이 아닌 규칙 기반(마스터 데이터 매칭+정규식)으로 직무 유형/기술명/부서명/가동일·기간/숙련도를 파싱, 결과는 `ParsedResourceQuery` 표준 스키마로 반환. SQL 조회는 이번 범위에서 수행하지 않음(사용자 확정, 아래 참고), 실 서버 pytest 검증 완료, 2026-07-04) |
| 파싱 결과 → SQL 조회 → 결과 요약 흐름 구현 | 완료 (`backend/app/services/ai_resource_search.py`(신규) `search_resources`가 whitelist 기반(`intent="resource_search"`)으로만 기존 `list_availability` repository를 호출 — LLM은 SQL 생성에 관여하지 않음. `POST /api/v1/ai/chat`에 연결해 조건이 인식되면 LLM을 거치지 않고 결정적 요약을 반환하도록 갱신, 실 서버 pytest 검증 완료, 2026-07-04. 기술 조건은 `list_availability`의 단일 `skill_id` 제약상 1개까지만 조회에 반영되고 나머지는 `skipped_skills`로 안내 — 다중 기술 AND 조회는 후속 확장 대상) |
| 권한 필터링 후 LLM 컨텍스트 전달 구현 | 완료 (`search_resources`가 반환하는 결과는 SCR-010 "가동 가능 인력" 데이터와 동일해, 응답 전 요청자 `PERM_JSON`의 `availability.view` 권한을 추가로 확인 — 없으면 조회를 실행하지 않고 안내 메시지만 반환. `app/api/deps.py`에 `has_permission` 유틸 신규 추가, 실 서버 검증 완료, 2026-07-04. 부서 단위 등 행(row) 단위 세부 범위 제한은 기존 `require_permission`과 동일한 한계로 이번 범위에서 다루지 않음) |
| 환각 방지 시스템 프롬프트 적용 | 완료 (`app/services/ai_chat.py`의 `call_llm`이 매 호출 시 시스템 메시지로 환각 방지 프롬프트를 함께 전달 — DB 조회 없이 답하는 이 경로에서 실존을 확인할 수 없는 사원/프로젝트/투입률 등 구체적 HR 데이터를 지어내지 말고 시스템 조회 기능 사용을 안내하도록 지침. `resource_search` 경로는 LLM을 거치지 않아 이미 환각 위험이 없어 대상 아님. 실 서버 pytest 검증 완료, 2026-07-04) |
| `POST /api/v1/ai/chat` 엔드포인트 구현 | 완료 (1차 범위 — LLM 단순 호출/응답만 구현, 조건 파싱·DB 조회는 제외, 권한 `ai_chat.view`(전 역할), 실 서버 검증 완료, 2026-07-04) |
| AI Chat 화면 구현 (`/ai-chat`) | 완료 (기존 프로토타입의 SQL·결과 테이블 표시용 목데이터 제거, 자유 대화형 UI를 실 API로 연동, 실 서버 검증 완료, 2026-07-04) |
| 테스트 질의 10개 이상 검증 (직무 유형 포함) | 완료 (`backend/tests/test_ai_chat_e2e.py`(신규) — 사용자가 확정했던 예시 질의 10개(직무 유형·기술·부서·가동일 조건 포함)를 `POST /api/v1/ai/chat` 전체 경로(파싱→권한 확인→조회→응답)로 검증, 전부 LLM을 거치지 않고 결정적 요약을 반환함을 확인. 일반 대화 1건이 LLM 경로로 정상 폴백되는 회귀 케이스도 함께 추가. 검증 중 응답 문구의 "가동률"이 실제로는 "가동 가능률"(`AVAIL_RT`)을 가리켜 의미가 반대로 읽히는 표기 오류를 발견해 함께 수정, 실 서버 검증 완료, 2026-07-04) |

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
| **개발 상태** | 진행 중 |
| **진행률** | 20% |
| **일정 상태** | 정상 |

**주요 작업**

| 작업 | 상태 |
|---|---|
| `HR_AVAIL_SNAP_GEN` 배치 구현 (매일 01:00 가동가능 스냅샷 생성) | 완료 (`backend/app/repositories/hr_avail_snap.py`의 `generate_avail_snap`, `backend/app/services/avail_snap_gen.py`의 `run_avail_snap_gen`(`SYS_BATCH_HIS` 이력 기록 포함), `backend/app/worker.py`(APScheduler `BlockingScheduler`, KST 01:00 cron) 신규 구현. 실 서버 컨테이너(`worker` 서비스)에서 스케줄러 정상 기동 확인 + 배치 함수 수동 실행으로 재직 사원 전체 스냅샷 생성 및 재실행 시 중복 없음(멱등) 확인, 2026-07-04) |
| `PJT_ASGN_END_ALERT` 배치 구현 (매주 금요일 17:00 종료 예정 알림) | 완료 (`backend/app/repositories/pjt_asgn_his.py`의 `list_ending_soon_assignments`, `backend/app/services/asgn_end_alert.py`의 `run_asgn_end_alert`(`SYS_BATCH_HIS` 이력 기록), `backend/app/services/teams_notify.py`(신규, Teams Incoming Webhook 전송) 구현, `app/worker.py`에 매주 금 17:00(KST) cron 등록. **`TEAMS_WEBHOOK_URL`이 `.env`에 미설정 상태라 실제 Teams 알림 전송은 검증하지 못함** — 웹훅 URL 미설정 시 배치 자체는 정상 실행하고 전송만 건너뛰도록 구현(코드 경로는 실 서버에서 확인), 실제 발송 검증은 후속 조치 필요(§9 참조). 실 서버 컨테이너에서 배치 실행·`SYS_BATCH_HIS` 기록·목데이터 대상 실제 종료 예정 건수 정상 판별 확인, 2026-07-04) |
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
| 종료 예정일 관리 | `ASGN_END_DT` 조회·알림 | 완료 (배치 로직·`SYS_BATCH_HIS` 기록 완료, 2026-07-04 — `TEAMS_WEBHOOK_URL` 미설정으로 실제 Teams 전송 자체는 미검증, §9 참조) | 높음 | `PJT_ASGN_HIS`, `PJT_ASGN_END_ALERT` 배치 | 30일 이내 종료 예정 알림 |
| 가동 가능일 자동 계산 | `HR_AVAIL_SNAP` 기반 산정 | 완료 (즉시 계산 API `GET /api/v1/availability/{empl_id}` 완료, 2026-07-03 + 매일 01:00 자동 스냅샷 생성 배치 `HR_AVAIL_SNAP_GEN`(`app/services/avail_snap_gen.py`, `app/worker.py`) 완료, 2026-07-04) | 높음 | `availability.py`, `HR_AVAIL_SNAP_GEN` 배치 | 투입률 0%=AVAILABLE(기준일), 1~99%=PARTIAL(기준일), ≥100%=FULL(MAX(종료일)+1, 종료일 NULL 시 품질경고) — `PROPOSED` 제외, 상세는 `backend/docs/AVAILABILITY_CALC_SPEC.md` |
| 즉시 투입 가능 인력 조회 | `AVAIL_STAT_CD='AVAILABLE'` 필터 | 완료 (`GET /api/v1/availability`, 직무 유형·부서 필터 포함, 실 서버 검증 완료 — 2026-07-04) | 높음 | `availability.py`, `hr_avail_snap.py` | 직무 유형 필터 포함 |
| 기술 기반 인력 검색 | 기술·숙련도·직무 복합 검색 | 예정 | 높음 | `recommendations.py` | `HR_EMPL_SKILL_REL` + `HR_JIKMU_MST` 조인 — `GET /availability`는 직무 유형만 지원, 기술·숙련도 필터는 별도 구현 필요 |
| 프로젝트 종료 예정자 조회 | 이번 달/30일 이내 종료 예정자 | 예정 | 높음 | `reports.py`, `PJT_ASGN_HIS` | |
| 팀별 가동률 조회 | 부서별 평균 `TOT_ALLOC_RT` | 예정 | 중간 | `dashboard.py`, `HR_AVAIL_SNAP` | |
| 리소스 추천 | `PJT_RCMD_RSLT` 점수 기반 후보 추천 | 완료 (`POST /api/v1/resource-requests`, `POST /api/v1/recommendations/score`, `GET /api/v1/recommendations/{req_id}` 구현, 실 서버 검증 완료 — 2026-07-04) | 중간 | `recommendations.py`, `pjt_rcmd_rslt.py` | 6개 항목 가중 점수(직무15%+기술35%+숙련도25%+가동일15%+유사경험7%+역할적합도3%) — 항목별 세부 산정 공식은 설계서에 없어 MVP 해석 적용, §9 참조 |
| AI 질의응답 | 자연어 → 조건 파싱 → SQL 조회 → 요약 | 완료 (LLM 단순 호출/응답(`ai_chat.py`, 환각 방지 시스템 프롬프트 포함) + 규칙 기반 조건 파싱(`ai_parser.py`) + whitelist 기반 SQL 조회·결과 요약(`ai_resource_search.py`) + 권한 필터링(`availability.view` 확인) + 엔드투엔드 질의 검증(`test_ai_chat_e2e.py`, 10개 질의) 전부 완료, Phase 6 100%, 2026-07-04) | 중간 | `ai_chat.py`, `ai_parser.py`, `ai_resource_search.py`, `POST /api/v1/ai/chat` | Phase 6 |
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
- **기술 관리 화면 구현 — 목데이터를 실 API로 연동 (§8 다음 작업 1번)** — 기존 저장소에 이미 있던 `frontend/app/(app)/skills/page.tsx`(검색/그룹/사용여부 필터, 등록·수정 모달까지 UI로는 완성되어 있었으나 전부 `lib/mock-data.ts` 기반)를 백엔드 `HR_SKILL_MST` API(조회/등록/수정, `backend/app/api/v1/skills.py`)로 연동. 백엔드는 이미 완전히 구현되어 있어 API 신규 작성 없이 프론트엔드만 재작성. `GET /skills`가 `use_yn` 생략 시 사용중(true)인 기술만 반환하는 기본 동작이라 "전체" 필터를 지원하기 위해 `use_yn=true`/`use_yn=false` 두 응답을 병렬 조회해 병합하는 방식 채택(백엔드 기본 동작은 다른 화면에 영향 없도록 변경하지 않음). "보유 인원" 컬럼은 별도 집계 API 없이 `GET /employee-skills`(전체) 조회 결과를 `SKILL_ID` 기준으로 클라이언트에서 카운트해 계산. 설계서(SCR-005)가 요구하는 "비활성 처리"는 `DELETE` 엔드포인트가 없어 기존 `PATCH /skills/{skill_id}`에 `USE_YN` 토글 요청을 보내는 방식으로 재사용(신규 엔드포인트 불필요). `frontend/lib/api.ts`에 `apiPost`/`apiPatch` 공통 헬퍼 신규 추가(기존 `apiGet`과 동일 패턴, 실패 시 서버 `detail` 메시지를 그대로 노출해 409 등 검증 오류를 화면에 표시). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 `POST /skills`로 임시 기술 1건 등록(201), `PATCH`로 `USE_YN` 토글(사용중→미사용) 확인, `use_yn=false` 목록 조회에 정상 반영됨을 확인, `/skills` 페이지 200 렌더링 확인. 검증 중 **`SKILL_NM`에 DB 유니크 제약이 없어 동일 이름으로 등록해도 409가 아닌 201이 반환됨을 발견**(설계서는 "기술명 중복 시 오류" 요구하나 현재 미충족) — §9 리스크로 신규 기록, 검증에 사용한 임시 데이터는 SQL로 삭제. 이번 작업은 프론트엔드 전용이라 백엔드 pytest 스위트는 변경 없이 21개 그대로 유지·통과 확인. §4 Phase 4 "기술 관리 화면 구현" 항목 완료로 갱신(진행률 50%→56%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거
- **직무 유형 관리 화면 구현 — 목데이터를 실 API로 연동, 등록/수정 API 신규 추가 (§8 다음 작업 1번)** — 기존 저장소에 이미 있던 `frontend/app/(app)/job-types/page.tsx`(검색/그룹/사용여부 필터, 등록·수정 모달까지 UI로는 완성되어 있었으나 전부 `lib/mock-data.ts` 기반)를 백엔드 `HR_JIKMU_MST` API로 연동. **기술 관리 화면과 달리 등록/수정 API 자체가 없어**(`GET /job-types` 조회만 존재) 신규 작성 — `backend/app/schemas/hr_jikmu_mst.py`에 `JobTypeCreate`/`JobTypeUpdate` 추가, `backend/app/repositories/codes.py`에 `get_job_type`/`create_job_type`/`update_job_type` 추가, `backend/app/api/v1/codes.py`에 `POST`/`PATCH /api/v1/job-types`(권한: `require_permission("job_types", "create"/"update")` — 기존 조회 API의 `codes.view`와 다른 권한 키, `PERMISSION_MATRIX.md` "job_types" 섹션 기준) 추가, `skills.py`/`employees.py` 패턴과 동일하게 `record_audit` 연동. `HR_JIKMU_MST.JIKMU_CD`는 모델에 이미 UNIQUE 제약이 있어(기술명과 달리) 중복 등록 시 `IntegrityError`를 잡아 409로 정상 변환됨을 검증으로 확인. 프론트엔드는 skills 화면과 동일하게 `use_yn=true`/`false` 병렬 조회로 "전체" 필터 지원, 직무 코드는 등록 시에만 입력받고 수정 폼에서는 제외(설계서 SCR-006 기준 직무 코드는 수정 대상 아님). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 `POST /job-types` 등록(201), 동일 코드 재등록 시 409(스키마 유니크 제약 정상 동작 확인 — 기술 관리 화면에서 발견한 `SKILL_NM` 무결성 문제와 대조됨), `PATCH`로 `USE_YN` 토글 확인, `/job-types` 페이지 200 렌더링 확인, `SYS_AUDIT_LOG`에 `CREATE`/`UPDATE` 기록 확인. `backend/tests/test_codes.py`(신규)에 등록/수정/중복 409/404/VIEWER 403/VIEWER 조회 가능 5개 케이스 추가(pytest 21→26개 전부 통과). 검증에 사용한 임시 데이터는 SQL로 삭제. §4 Phase 4 "직무 유형 관리 화면 구현" 항목 완료로 갱신(진행률 56%→63%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거
- **긴급 수정 — SSH 터널 접속 시 로그인 불가 (사용자 보고)** — 사용자가 "SSH 터널로 `localhost:3030` 접속 시 로그인 화면에서 '서버에 연결할 수 없습니다' 오류, `hrm-api` 로그에도 요청 기록 자체가 없다"고 보고. 프론트엔드 JS 번들을 직접 확인해 `NEXT_PUBLIC_API_BASE_URL`(빌드 시점에 고정되는 값)이 서버의 LAN IP(`http://192.168.0.87:8000`)로 절대경로 고정되어 있음을 확인 — SSH 로컬 포트 포워딩(`-L`)은 클라이언트가 `localhost:포트`로 접속할 때만 가로채므로, 클라이언트 JS가 LAN IP를 직접 호출하면 터널을 거치지 않고 클라이언트 PC에서 그 IP로 직접 연결을 시도하다 실패하는 구조였음(같은 LAN에 있지 않으면 연결 자체가 안 됨) — 이는 CORS 문제가 아니라 순수 네트워크 도달 불가 문제로, 요청이 서버에 도달하기 전에 실패해 `hrm-api` 로그에 기록이 없는 것과도 일치. **구조적 해결**: `frontend/next.config.mjs`에 `rewrites()` 추가 — `/api/v1/*` 요청을 Next.js 서버가 Docker 내부망의 `api:8000`(백엔드 컨테이너, 서비스명으로 내부 DNS 해석) 컨테이너로 대신 전달하도록 프록시 구성. 프론트엔드 코드(`lib/api.ts`, `lib/auth.ts`)는 이미 `NEXT_PUBLIC_API_BASE_URL`이 빈 값이면 상대 경로(`/api/v1/...`)로 호출하도록 되어 있어 코드 변경 없이 프록시를 자동으로 타게 됨. 사용자가 `.env`의 `NEXT_PUBLIC_API_BASE_URL`을 빈 값으로 직접 변경(수정 금지 파일이라 AI가 직접 수정하지 않음, 값 변경만 안내), 이후 `docker compose up -d --build web` 재빌드 진행. **실 서버에서 실제 검증**: 재빌드 후 컴파일된 JS 번들에 절대 IP가 완전히 사라짐을 확인, `curl http://localhost:3030/api/v1/auth/login`(3030 포트 하나만으로 프록시 경유) 200 정상 토큰 발급 확인, `/login` 페이지 200 렌더링 확인, `pytest` 26개 그대로 통과 확인. 이 변경으로 **LAN IP 직접 접속과 SSH 터널(3030 포트 하나만 필요) 두 접속 방식을 하나의 빌드로 동시에 지원**하게 되어, 접속 방식이 여러 개일 때 매번 재빌드가 필요했던 기존 구조적 한계도 함께 해소됨. 백로그 §8 큐에 있던 예정 작업이 아니라 사용자가 보고한 장애의 긴급 수정이라 별도 순번 없이 기록
- **프로젝트 목록/상세 화면 구현 — 목데이터를 실 API로 연동, 단건 조회 API 신규 추가 (§8 다음 작업 1번)** — 기존 저장소에 이미 있던 `frontend/app/(app)/projects/page.tsx`(검색/상태 필터, 등록 모달)와 `frontend/app/(app)/projects/[id]/page.tsx`(개요/투입 유형 구성/투입 인력 목록 탭)를 백엔드 `PJT_MST`/`PJT_ASGN_HIS` API로 연동. 사원 상세와 마찬가지로 프로젝트 단건 조회 API가 없어(목록/등록/수정만 존재) `backend/app/api/v1/projects.py`에 `GET /projects/{pjt_id}`(신규, 기존 `get_project` 리포지토리 재사용, `require_permission("projects","view")`, 404 처리) 추가. 목록 화면은 `GET /projects`(페이지네이션 응답)와 진행 중(`ACTIVE`) 투입 이력을 집계해 "투입 인원" 컬럼을 계산, "프로젝트 등록" 모달은 `POST /projects`로 실제 연동(설계서 SCR-007 목업에는 없었으나 백엔드 스키마상 필수인 `PJT_CD` 입력 필드를 등록 폼에 추가, 사유 주석 명시 — `PJT_CD`는 모델에 UNIQUE 제약이 있어 중복 시 409 정상 반환 확인). 상세 화면은 `GET /projects/{pjt_id}` + `GET /assignments?pjt_id=`(투입 이력) + `GET /employees`/`departments`/`job-types`(사원명·부서명·직무명 조인, 사원 상세 화면과 동일한 클라이언트 조인 패턴 재사용)를 병렬 조회해 개요·투입 유형 구성·투입 인력 테이블을 실 데이터로 렌더링, 총 투입 인원/평균 투입률은 `ASGN_STAT_CD='ACTIVE'` 건 기준으로 계산. **범위를 의도적으로 축소한 부분**: "수정"/"종료처리"/"인력 투입" 버튼은 사원 상세 화면과 동일한 이유(편집 폼을 이번 범위에서 다루지 않음)로 제외, 조회 전용으로 제공 — 별도 §9 리스크는 추가하지 않음(사원 상세와 동일한 유형의 기존 리스크로 통합 가능하나 화면이 달라 세부 후속 작업은 프로젝트 CRUD 착수 시 재확인). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: `docker compose up -d --build api web` 재빌드 성공, `POST /projects` 등록(201), 동일 코드 재등록 시 409, `GET /projects/{pjt_id}` 200/존재하지 않는 ID 404, `/projects`·`/projects/{pjt_id}` 페이지 200 렌더링 확인. `backend/tests/test_projects.py`(신규)에 등록/수정/상세조회/404/중복 409/VIEWER 조회 가능 5개 케이스 추가(pytest 26→31개 전부 통과). 검증에 사용한 임시 데이터는 SQL로 삭제. §4 Phase 4 "프로젝트 목록/상세 화면 구현" 항목 완료로 갱신(진행률 63%→69%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거
- **투입 관리 화면 구현 — 목데이터를 실 API로 연동, 등록 모달 신규 추가 (§8 다음 작업 1번)** — 기존 저장소에 이미 있던 `frontend/app/(app)/assignments/page.tsx`(검색/유형/상태 필터, 공수 초과 배정 감지 배너)를 백엔드 `PJT_ASGN_HIS` API로 연동. 투입 관리 API(`GET/POST/PATCH /api/v1/assignments`, ALLOC_RT 100% 초과 검증 포함)는 이미 완전히 구현되어 있어 백엔드 변경 없이 프론트엔드만 재작성. `GET /assignments` + `GET /employees`/`projects`(사번·성명·프로젝트명 조인, 다른 상세 화면들과 동일한 클라이언트 조인 패턴 재사용)를 병렬 조회해 목록을 실 데이터로 렌더링, 공수 초과 배정 감지 배너도 목데이터 계산 로직을 `ASGN_STAT_CD='ACTIVE'` 건의 `ALLOC_RT` 합계 기준 실 데이터 계산으로 교체. **기존 프로토타입에 없던 "투입 등록" 모달을 설계서(SCR-009) 기준으로 신규 작성** — 사원/프로젝트 검색 선택(Select), 프로젝트 유형(RUNNING/COMMITTED/PROPOSED), 역할·기간·투입률·비고 입력 후 `POST /assignments` 호출, 동일 사원·겹치는 기간 합계 100% 초과 시 백엔드가 반환하는 409 오류 메시지를 폼에 그대로 노출(설계서의 "예상 총 투입률 미리보기"는 별도 계산 로직이 필요해 이번 범위에서 제외, 서버 검증 메시지로 대체 — 사유 주석 명시). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 임시 부서·사원·프로젝트로 투입 60% 등록 성공 후 동일 기간 50% 추가 등록 시 409(합계 110% 초과) 정상 거부 확인, `/assignments` 페이지 200 렌더링, 목록 조회 응답에 사번/성명/프로젝트명 조인 결과 정상 확인. 검증에 사용한 임시 데이터는 SQL로 삭제. 백엔드 변경 없어 pytest는 31개 그대로 유지. §4 Phase 4 "투입 관리 화면 구현" 항목 완료로 갱신(진행률 69%→75%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거
- **가동 가능 인력 조회 화면 구현 — 목데이터를 실 API로 연동, 일괄 조회 API 신규 추가 (§8 다음 작업 1번)** — 기존 저장소에 이미 있던 `frontend/app/(app)/availability/page.tsx`(즉시/부분/기간 3개 탭, 검색·조직 필터)를 백엔드 가동률 계산 API로 연동. 기존 `GET /api/v1/availability/{empl_id}`는 사원 1명씩만 계산하는 단건 API라 화면에 필요한 "전체 사원 목록 조회"가 불가능해, `backend/app/repositories/hr_avail_snap.py`에 `list_availability`(신규) 추가 — 재직 사원 전체의 투입 이력을 한 번에 조회한 뒤 파이썬에서 사원별로 묶어 계산해 N+1 쿼리를 방지했다. 기존 `compute_availability`(단건)와 계산 로직이 완전히 같아야 하므로 `_classify` 헬퍼로 판정 로직을 추출해 두 함수가 공유하도록 리팩터링(동작 변경 없는 순수 추출, 기존 단건 API 회귀 위험 최소화). `backend/app/api/v1/availability.py`에 `GET /availability`(신규, `jikmu_id`/`dept_id`/`snap_dt` 필터, `require_permission("availability","view")`) 추가 — 백로그 항목이 명시한 "직무 유형 필터"를 여기서 지원. 프론트엔드는 이 신규 API + `employees`/`departments`/`job-types`/`skills`/`employee-skills`(다른 화면들과 동일한 클라이언트 조인 패턴)를 병렬 조회해 탭(AVAILABLE=즉시/PARTIAL=부분/FULL=기간)·조직·직무 유형·검색 필터를 실 데이터로 구현, 탭 구성이 `AVAILABILITY_CALC_SPEC.md`의 `AVAIL_STAT_CD` 3종과 정확히 1:1 대응됨을 확인해 별도 매핑 없이 그대로 사용. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 투입 이력이 없는 임시 사원이 `AVAILABLE`로, 활성 투입 50%가 있는 사원이 `PARTIAL`로 정확히 분류됨을 확인, `dept_id`/`jikmu_id` 필터가 대상 사원을 정확히 포함/제외함을 확인, `/availability` 페이지 200 렌더링 확인. `backend/tests/test_availability.py`(신규)에 즉시 가동 분류/부분 가동 분류/직무유형 필터/VIEWER 접근 제한(설계서상 VIEWER 제외 확인) 4개 케이스 추가(pytest 31→35개 전부 통과). 검증에 사용한 임시 데이터는 SQL로 삭제. §4 Phase 4 "가동 가능 인력 조회 화면 구현" 항목 완료로 갱신(진행률 75%→81%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거
- **리소스 추천 화면 구현 — 백엔드 API 신규 구현(추천 알고리즘 최초 구현) + 프론트엔드 실 연동 (§8 다음 작업 1번)** — 다른 Phase 4 화면들과 달리 이번 항목은 백엔드 API 자체가 전혀 없어(모델·스키마 출력 타입만 존재) 추천 로직을 처음부터 구현. **`PJT_RSRC_REQ`(리소스 요청)**: `ResourceRequestCreate` 스키마·`repositories/pjt_rsrc_req.py`·`POST /api/v1/resource-requests`(권한 `recommendations.create`) 신규. **`PJT_RCMD_RSLT`(추천 결과)**: `repositories/pjt_rcmd_rslt.py`에 6개 항목 가중 점수(직무 유형 일치 15%+기술 매칭 35%+숙련도 25%+가동 가능일 15%+유사 경험 7%+역할 적합도 3%, 합 100점) 산정 로직 신규 구현 — 재직 사원 전체를 대상으로 요청 조건과 대조해 채점 후 상위 10명을 저장(재실행 시 이전 결과 삭제 후 재저장). 가동 가능일 판정은 §8 앞서 구현한 `list_availability`(전 사원 가동률 일괄 계산)를 그대로 재사용. `POST /api/v1/recommendations/score`(점수 실행+저장), `GET /api/v1/recommendations/{req_id}`(과거 결과 조회) 추가, `api/v1/router.py`에 라우터 등록. **설계서에 항목별 세부 산정 공식이 없어 MVP 해석을 적용**(직무 일치는 이진 판정, 기술 매칭은 보유 비율, 숙련도는 매칭 기술 평균, 가동일은 희망일 이내 여부 이진 판정, 유사경험은 요청 역할명과 일치하는 과거 완료 투입 건수 — §9 리스크로 기록, 운영팀 확인 필요). 기존 §9 리스크 "PJT_RCMD_RSLT 추천 점수 가중치 표기 불일치"도 이번 구현으로 로드맵 수치 기준 확정되어 해소 처리. 프론트엔드는 기존 프로토타입(`frontend/app/(app)/recommendations/page.tsx`, 요건 입력 폼+결과 카드 UI는 이미 완성)을 실 API로 재작성 — 프로젝트/직무 유형/기술 Select를 실 마스터 데이터로 교체, "추천 인력 조회" 클릭 시 리소스 요청 등록→점수 계산을 순차 호출 후 결과에 사원명·직무명·보유기술을 조인해 표시. **범위를 의도적으로 축소한 부분**: 설계서의 다중 기술 칩 선택은 단일 선택으로 축소(백엔드는 배열을 이미 지원), "이 후보로 투입 요청" 버튼(실제 투입 등록 연동)은 결과 조회까지만 구현하고 제외 — 둘 다 §9 리스크로 기록. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 임시 부서·사원·프로젝트로 리소스 요청 등록 → 추천 실행 → 해당 사원이 결과에 포함되고 투입 이력이 없어 가동일 점수(15점) 만점 획득 확인, 동일 요청 재실행 시 이전 결과가 정확히 교체됨을 확인, 존재하지 않는 요청으로 실행 시 404, `/recommendations` 페이지 200 렌더링 확인. `backend/tests/test_recommendations.py`(신규)에 요청 등록/점수 실행 및 조회/재실행 시 결과 교체/404/VIEWER 403 5개 케이스 추가(pytest 35→40개 전부 통과). 검증에 사용한 임시 데이터는 SQL로 삭제. §4 Phase 5(리소스 검색 및 추천 기능 구축, 지금까지 0%였던 별도 Phase) "주요 작업" 표의 관련 5개 항목(즉시 투입 가능 인력 조회 API·추천 점수 산정 로직·`PJT_RSRC_REQ` API·`PJT_RCMD_RSLT` API·리소스 추천 화면)을 완료로 갱신, Phase 5 진행률 0%→75%·상태 "예정→진행 중"으로 전환(§3 전체 로드맵 표 동일 갱신 — "즉시 투입 가능 인력 조회 API"와 "가동 가능 인력 화면 구현"은 지난 턴에 이미 완료되었으나 이 표에 반영이 누락되어 있던 것을 이번에 함께 바로잡음), §5 기능별 구현 상태·§11 체크리스트 항목 완료 체크, §8 큐에서 완료 항목 제거
- **AI Chat 화면 구현 — LLM 연동 1차 범위(사용자 확정: 단순 호출/응답) 신규 구현 (§8 다음 작업 1번)** — 직전 턴에 사용자가 `.env`에 DeepSeek 연동 정보를 이미 설정해뒀음을 확인하고 실제 인증 호출로 연결 가능함을 검증한 데 이어, 이번 턴에 실제 구현을 진행. `backend/app/core/config.py`(`Settings`)에 `LLM_PROVIDER`/`DEEPSEEK_API_KEY`/`DEEPSEEK_BASE_URL`/`DEEPSEEK_MODEL_ID`/`OPENAI_API_KEY` 필드 신규 추가(그동안 `extra="ignore"`라 조용히 무시되고 있었음), `.env.example`도 실제 `.env` 구성(DeepSeek 기준)과 일치하도록 갱신(`.env` 자체는 수정하지 않음). `backend/app/services/ai_chat.py`(신규) — `call_llm(message)`가 `LLM_PROVIDER` 값으로 공급자를 분기하는 간단한 추상화(현재 DeepSeek만 지원, §4 Phase 6 "LLM 연동 인터페이스 추상화" 항목 충족), `httpx`로 DeepSeek `chat/completions`(OpenAI 호환) 호출, 실패 시 `LlmCallError`로 통일해 처리. `backend/app/schemas/ai_chat.py`(`ChatRequest`/`ChatResponse`), `backend/app/api/v1/ai_chat.py`(`POST /api/v1/ai/chat`, 권한 `ai_chat.view` — `PERM_JSON`상 전 역할 허용과 일치, LLM 실패 시 502) 신규 작성, `api/v1/router.py`에 등록. **1차 구현 범위는 사용자가 명시적으로 확정한 대로 LLM 단순 호출/응답만 다룸** — 자연어 조건 파싱·SQL 조회 연동·권한 필터링 기반 컨텍스트 전달·환각 방지 프롬프트는 후속 작업으로 분리(§4 Phase 6 표·§9-1 체크리스트에 반영). 프론트엔드는 기존 프로토타입(`frontend/app/(app)/ai-chat/page.tsx`)의 정적 캔드 응답(키워드 매칭 목데이터, SQL·결과 테이블 표시)을 제거하고 `POST /api/v1/ai/chat` 실 호출로 교체 — 응답 대기 중 로딩 표시, 실패 시 에러 메시지를 대화 버블로 표시. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 실제 DeepSeek API를 호출해 정상 답변 수신 확인, 무인증 401, 빈 메시지 422, `/ai-chat` 페이지 200 렌더링 확인. `backend/tests/test_ai_chat.py`(신규)에 정상 응답/무인증/빈 메시지/LLM 실패 시 502/VIEWER 접근 가능 5개 케이스 추가 — 반복 실행 가능성과 오프라인 실행을 위해 `call_llm`을 모킹해 실제 네트워크 호출 없이 검증(실제 DeepSeek 연동 자체는 수동 curl로 이미 확인)(pytest 40→45개 전부 통과). §4 Phase 6(AI 질의응답 연동, 지금까지 0%였던 별도 Phase) "주요 작업" 표의 관련 3개 항목(LLM 연동 인터페이스 추상화·`POST /api/v1/ai/chat`·AI Chat 화면) 완료로 갱신, Phase 6 진행률 0%→38%·상태 "예정→진행 중"으로 전환(§3 전체 로드맵 표 동일 갱신), §5·§11 체크리스트 항목 완료 체크, §9-1 체크리스트에 AI Chat 후속 항목 4건 추가, §8 큐에서 완료 항목 제거
- **리포트 화면 구현 — 주간/월간 리포트 백엔드 API 신규 구현 (§8 다음 작업 1번)** — 백엔드에 리포트 관련 API가 전혀 없어(모델도 없음) 신규 구현. 설계서(SCR-013)가 "주간 리포트와 월간 리포트는 기간 단위만 다를 뿐 동일한 구조"라고 명시한 점에 착안해, `backend/app/repositories/reports.py`(신규)에 `build_report(db, as_of)` 공용 함수를 작성 — 이미 구현되어 있던 대시보드 집계 함수(`get_summary`/`get_dept_utilization`/`get_data_quality`, `app/repositories/dashboard.py`)를 그대로 재사용하고, 리포트 전용 위젯인 "기술별 인력 분포 Top 10"만 `get_skill_distribution_top`으로 신규 추가(`HR_EMPL_SKILL_REL`+`HR_SKILL_MST` 조인, 보유 인원 내림차순 상위 10개). `backend/app/schemas/reports.py`(`ReportOut`, 기존 `DashboardSummaryOut`이 아닌 리포트 전용 스키마로 분리하되 `DeptUtilizationItem`은 재사용), `backend/app/api/v1/reports.py`(신규) — `GET /reports/weekly?week=YYYY-Www`(ISO 주차 파싱, `date.fromisocalendar`), `GET /reports/monthly?month=YYYYMM` 둘 다 동일한 `build_report`를 호출(중복 로직 없음), 잘못된 형식은 422, 권한 `require_permission("reports","view")`(설계서 접근 권한 "A H P E"와 동일하게 TEAM_LEAD/VIEWER 제외 — 기존 Seed `PERM_JSON`과 이미 일치 확인). 과거 특정 주차/월의 스냅샷을 보관하지 않으므로(§9 기존 "대시보드가 HR_AVAIL_SNAP 대신 실시간 계산 사용" 리스크와 동일 제약), 지정 시점 기준으로 현재 데이터를 즉시 재계산하는 방식을 그대로 채택(사유 주석 명시). **범위를 의도적으로 축소한 부분**: 설계서 탭 3 "월별 가동률 통계"(인원별 프로젝트 투입 행+월별 12개 컬럼+3단계 조직 평균+100% 초과 경고 매트릭스)는 구조가 복잡해 이번 범위에서 제외하고 화면에 준비 중 안내만 표시, "리포트 수동 발송"(Teams Webhook)과 "Excel 내보내기"도 별도 인프라 연동이 필요해 제외 — 셋 다 §9 리스크로 기록. 프론트엔드는 기존 프로토타입(`frontend/app/(app)/reports/page.tsx`)의 탭 구성(가동률 매트릭스/인력 추이/기술 분포, 전부 목데이터)을 설계서 기준 탭(주간/월간/월별 통계)으로 재구성해 실 API 연동 — 주차/월 선택기(HTML5 `input[type=week/month]`)로 조회 시점 변경, 요약 6개 스탯 카드(전체인원/즉시가동/부분가동/풀투입/종료예정/직무미등록)+부서별 가동률+기술별 분포 차트 2종을 실 데이터로 렌더링. 기존 `SkillBarChart` 컴포넌트가 목데이터 직접 import 방식이던 것을 다른 차트들과 동일하게 `data` prop 기반으로 리팩터링. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 임시 부서·사원으로 `GET /reports/weekly`가 즉시 가동 인원·직무 미등록 수를 정확히 반영함을 확인, 잘못된 `week`/`month` 형식 422, `/reports` 페이지 200 렌더링 확인. `backend/tests/test_reports.py`(신규)에 기본 조회/신규 사원 반영 확인/잘못된 형식 422(주간·월간)/VIEWER 403 6개 케이스 추가(pytest 45→51개 전부 통과). 검증에 사용한 임시 데이터는 SQL로 삭제. §4 Phase 4 "리포트 화면 구현" 항목 완료로 갱신(진행률 81%→88%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐에서 완료 항목 제거
- **`HR_SKILL_MST` 표준 Seed 재작성 및 DB 반영 (사용자 요청)** — 기존 MVP 초안(BACKEND/FRONTEND/ARCHITECTURE/CLOUD/BUSINESS/DESIGN 6개 그룹, 55건, DB 미반영 상태)을 사용자 확정 기준의 13개 그룹(LANGUAGE/BACKEND/FRONTEND/MOBILE/DB/DATA/INFRA/SECURITY/ARCHITECTURE/QA/CONSULTING/PMO/BUSINESS(금융)) 110건으로 전면 재작성 — `backend/app/db/seed/hr_skill_mst_seed.py`. 기술명은 사원 목록 Excel Import "주요기술" 컬럼과 매핑될 수 있도록 표준 영문/일반 명칭 우선(예: "Java", "PostgreSQL", "SAP(ERP)"), BUSINESS 그룹은 금융 SI 도메인 지식(여신/수신/카드/보험/증권/외환/전자금융/자금세탁방지/바젤·IFRS/핀테크) 위주로 구성. **동일 (SKILL_GRP_CD, SKILL_NM) 조합 중복 방지**를 위해 Alembic 마이그레이션(`55106956dedf`, 신규)에서 `HR_SKILL_MST`에 `(SKILL_GRP_CD, SKILL_NM)` 복합 UNIQUE 제약(`uq_hr_skill_mst_grp_nm`)을 추가하고, Seed 삽입도 `INSERT ... ON CONFLICT DO NOTHING`으로 처리해 마이그레이션을 재실행하거나 이미 존재하는 조합을 다시 넣어도 중복 행이 생기지 않도록 구현 — 이 제약 추가로 기존 §9 리스크 "`HR_SKILL_MST.SKILL_NM`에 유니크 제약 없음"도 함께 해소(기술 관리 화면 검증 중 발견했던 미충족 상태를 정식으로 수정). 기존 테이블 생성 리비전(`28ce52377e32`)은 되돌리지 않고 새 리비전으로 제약+Seed만 추가하는 기존 패턴(`370c95546556` 등)을 그대로 따름. 검증 중 이전 세션에서 남아있던 테스트 잔여 데이터(`BACKEND/Python`, 비활성) 1건을 발견해 정리. **실 서버 컨테이너에서 `alembic upgrade head` 실제 실행으로 검증**(이전 Phase 2 마이그레이션들과 달리 이번에는 Docker 환경에 `alembic`이 있어 실제 적용 가능) — 적용 후 `HR_SKILL_MST` 110건/13개 그룹 정상 확인, `alembic downgrade -1`로 되돌린 뒤 다시 `upgrade head`로 재적용해 0건→110건 정상 복원 확인(멱등성 검증), 동일 조합 재삽입 SQL을 직접 실행해도 행 수가 늘지 않음을 확인. API 레벨에서도 동일 조합 재등록 시 409, 다른 그룹의 동일 이름은 201로 정상 허용됨을 curl로 확인. `backend/tests/test_skills.py`(신규 — 그동안 기술 관리 API에 전용 테스트가 없었음)에 등록/수정/중복 409(회귀 테스트)/동일 이름 다른 그룹 허용/VIEWER 403(설계서 접근 권한 "A H" 확인) 4개 케이스 추가(pytest 51→55개 전부 통과). §9 리스크 2건 해소("직원 기술 스택 표준화 기준 미정", "`SKILL_NM` 유니크 제약 없음"), §11 데이터베이스 체크리스트 "HR_SKILL_MST Seed 입력" 항목 완료 체크(Phase 2는 이미 100% 완료 상태라 진행률 변경 없음). `.env`/DESIGN 파일은 수정하지 않음
- **기술/직무유형 화면 그룹 필터 하드코딩 버그 수정 (사용자 질의)** — 사용자가 "각 화면의 검색 필터가 DB에서 조회되는지 하드코딩인지"를 질의해 전 화면을 감사 — `HR_SKILL_MST` 표준 Seed 재작성(바로 위 항목) 직후라 기술 관리(`/skills`) 화면의 "기술 그룹" 필터가 `frontend/lib/options.ts`에 하드코딩된 옛 7개 그룹만 사용해 새 Seed의 13개 그룹 중 다수가 필터로 선택 불가능한 상태임을 발견, 사용자 확인 후 즉시 수정. 하드코딩된 `skillGroupOptions`를 제거하고 화면에서 실제로 불러온 데이터의 `SKILL_GRP_CD` distinct 값으로 필터·등록 모달 그룹 목록을 동적 생성(`useMemo`). 직무 유형(`/job-types`) 화면의 "그룹" 필터도 동일한 문제 가능성이 있어 함께 점검·수정 — 단 등록/수정 모달은 설계서(SCR-006)가 명시한 고정 3종(TECHNICAL/MANAGEMENT/ANALYSIS)을 그대로 유지(신규 등록 시 그룹명 난립 방지 목적, 필터와는 별개 사안이라 분리 유지). 나머지 화면(가동 가능 인력·리소스 추천의 조직/직무유형/기술 필터)은 이미 실 API 기반이라 문제없음을 확인, 상태/유형 계열 필터(프로젝트 상태·투입 유형 등)는 DB CHECK 제약과 동일한 고정 열거값이라 하드코딩이 정상 설계임도 함께 확인. 백엔드 변경 없음(프론트엔드 전용), 재빌드 후 `/skills`·`/job-types` 페이지 200 렌더링 확인, pytest 55개 그대로 통과
- **설정 화면 구현 — 사용자 관리·감사 로그 조회 백엔드 API 신규 구현 (§8 다음 작업 1번)** — 기존 저장소에 `/settings` 화면(일반설정/사용자관리/감사로그 3개 탭, `UsersTable`/`AuditLogTable` 컴포넌트로 UI는 이미 완성되어 있었으나 전부 `lib/mock-data.ts` 기반)이 있었으나 백엔드 API가 전혀 없어 신규 구현. **사용자 관리(SCR-015)**: `backend/app/schemas/sys_user_mst.py`에 `UserCreate`(비밀번호 정책 검증 — 8자 이상+영문+숫자+특수문자, `field_validator`로 구현) 추가, `repositories/sys_user_mst.py`에 `list_users`/`create_user` 추가, `backend/app/api/v1/users.py`(신규) — `GET /users`(목록), `POST /users`(등록, 비밀번호는 기존 `core/security.hash_password`로 해시 저장 후 평문 필드 제외), `GET /users/roles`(신규 — 등록 모달의 "역할" 드롭다운용, 기존 `SYS_ROLE_MST`에 목록 조회 API가 아예 없어 `repositories/sys_role_mst.py`도 함께 신규 작성), 권한 `settings_users.view/create`(설계서 접근 권한 "A(Admin 전용)"과 기존 Seed `PERM_JSON`이 이미 일치). **감사 로그(SCR-016)**: `repositories/sys_audit_log.py`에 `list_audit_logs`(신규 — `SYS_USER_MST`와 조인해 화면에 필요한 `USER_LGID` 함께 반환, 사용자 로그인ID/행위코드/대상테이블/기간 필터 지원) 추가, `schemas/sys_audit_log.py`에 `AuditLogListItemOut`/`AuditLogListResponse`(기존 `PaginatedResponse` 재사용) 추가, `backend/app/api/v1/audit_logs.py`(신규) — `GET /audit-logs`, 권한 `settings_audit_logs.view`(Admin 전용). 두 라우터 모두 `api/v1/router.py`에 등록. **범위를 의도적으로 축소한 부분**: 계정 수정(`PATCH /users/{id}`)·비활성화(`DELETE /users/{id}`)는 이번 범위에서 제외(등록·조회까지만 구현), 감사 로그 Excel 내보내기(`GET /audit-logs/export`)도 제외 — 둘 다 §9 리스크로 기록. 프론트엔드는 `UsersTable`/`AuditLogTable` 두 컴포넌트를 실 API로 재작성 — 사용자 목록은 역할·활성상태 필터를 실 `SYS_ROLE_MST` 데이터 기준으로 동적 생성(스킬/직무유형 화면과 동일한 원칙 적용), 감사 로그는 서버 측 필터(행위코드·사용자 검색)와 클라이언트 측 보강 검색을 함께 사용. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 사용자 등록(201, 응답에 비밀번호/해시 미노출 확인), 약한 비밀번호 422, 로그인 ID 중복 409, 감사 로그 목록 조회(56건 확인, 기존 세션에서 쌓인 실제 로그)·행위코드 필터 정상 동작 확인, `/settings` 페이지 200 렌더링 확인. 검증에 사용한 임시 사용자 계정은 SQL로 삭제. `backend/tests/test_users.py`·`test_audit_logs.py`(신규) 총 8개 케이스 추가(등록/약한 비밀번호 422/중복 409/VIEWER 403, 감사 로그 기본조회/필터/VIEWER 403 — pytest 55→63개 전부 통과). §4 Phase 4 "설정 화면 구현" 항목 완료로 갱신(진행률 88%→94%), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §9-1 체크리스트에서 "감사 로그 조회 API 없음" 항목 해소 처리, §8 큐에서 완료 항목 제거
- **Excel Import/Export UI 구현 — §8 큐 마지막 항목, 기존 백엔드 API 프론트엔드 연동 (§8 다음 작업 1번)** — 사원 목록 화면(SCR-003)에 Import/Export UI가 전혀 없었으나, 백엔드 `GET/POST /api/v1/employees/{export,import}`는 이전 세션에서 이미 구현·미검증 상태로 존재해 신규 프론트엔드 연동 작업으로 진행. `frontend/lib/api.ts`에 `apiUploadFile`(FormData 업로드)·`apiDownloadFile`(Blob 다운로드+`Content-Disposition` 파일명 파싱+브라우저 저장 트리거) 신규 추가, `ApiError`에 구조화된 검증 오류(`{total_rows, error_count, errors}`)를 담기 위한 선택적 `detail` 필드 추가. `frontend/components/employees/employee-import-dialog.tsx`(신규) — 파일 선택 후 업로드, 성공 시 신규/수정 건수 표시, 422 검증 실패 시 행별 오류(행/컬럼/값/사유) 테이블로 표시. `employees/page.tsx` 헤더에 "Excel 가져오기"/"Excel 내보내기" 버튼 추가(다른 화면들과 동일하게 클라이언트 측 권한 버튼 게이팅은 하지 않음 — 기존 전 화면 공통 패턴, 백엔드 `require_permission("employees","excel")`이 실제 차단 담당). **작업 중 실제 라우팅 버그 발견 및 수정**: `GET /export`가 `GET /{empl_id}`(UUID 경로 파라미터) 라우트보다 뒤에 등록되어 있어, FastAPI가 등록 순서대로 매칭하는 특성상 "export" 문자열이 UUID로 파싱 시도되어 실제로는 항상 422를 반환하고 있었음(한 번도 정상 동작한 적 없는 기존 버그) — `backend/app/api/v1/employees.py`에서 `/export`·`/import` 라우트 정의를 `/{empl_id}` 라우트보다 앞으로 이동해 수정. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 수정 전 재현(422 확인) → 수정 후 정상 동작 확인(Export가 지정된 헤더 순서의 xlsx 반환, 잘못된 값이 포함된 파일 Import 시 행 번호가 정확한 422 오류 목록 반환), `/employees` 페이지 200 렌더링 확인. `backend/tests/test_employees_excel.py`(신규, 라우팅 버그 회귀 방지 목적 명시) 2개 케이스 추가(pytest 63→65개 전부 통과). **알려진 한계**: 사원 목록 화면 자체는 여전히 목데이터 기반이라(§9-1 기존 항목과 동일 사안) Import 성공 후에도 화면 목록이 실시간으로 갱신되지는 않음 — 새로 만들지 않고 기존 항목을 그대로 참조. §4 Phase 4 "Excel Import/Export UI 구현" 항목 완료로 갱신(진행률 94%→100%, Phase 4 전체 완료), §3 전체 로드맵 표 동일 갱신, §11 항목 완료 체크, §8 큐가 이번 항목 제거로 전부 소진(빈 큐)
- **직무 유형·기술·숙련도 복합 필터 검색 API 구현 (§8 다음 작업 1번)** — Phase 4 완료로 재구성된 Phase 5 잔여 항목. 기존 `GET /api/v1/availability`(SCR-010 "가동 가능 인력")는 `jikmu_id`/`dept_id` 필터만 지원하고 기술·숙련도 필터가 없어, `backend/app/repositories/hr_avail_snap.py`의 `list_availability`에 `skill_id`/`min_prfcy_levl` 파라미터를 추가 — 대상 사원 필터링 단계에서 `HR_EMPL_SKILL_REL`(`SKILL_ID` 일치 + `PRFCY_LEVL >= min_prfcy_levl`)을 만족하는 사원만 포함하도록 서브쿼리로 구현(기존 N+1 방지용 일괄 계산 구조는 그대로 유지). `backend/app/api/v1/availability.py`에 동일 쿼리 파라미터 추가(`min_prfcy_levl`은 1~5 범위 검증, `skill_id` 없이 단독 지정 시 무시하도록 리포지토리 주석에 명시). 프론트엔드 `/availability` 화면은 기존에 이미 클라이언트 측 검색어로 보유 기술명을 필터링하고 있어 이번 범위에서는 화면 변경 없이 백엔드 API만 구현(최소 단위 원칙). **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 임시 사원 2명 중 1명에게만 기술을 등록한 뒤 `skill_id`+`min_prfcy_levl=3` 조회 시 해당 사원만 포함되고, `min_prfcy_levl=5`(실제 등록값 4 미만 요구)로 올리면 제외됨을 확인. `backend/tests/test_availability.py`에 케이스 1개 추가(pytest 65→66개 전부 통과). Phase 5 진행률 75%→88%로 갱신(8개 항목 중 7개 완료, 잔여 1개는 Phase 7 배치 선행 필요), §3/§4/§11 항목 갱신, §8 큐를 다음 순서인 Phase 6(AI 질의응답 연동, 38%)의 "자연어 조건 파싱 구현"으로 재구성 — 단 이 항목은 사용자가 이전에 "AI Chat 화면 구현과 분리해 별도 후속 작업으로 진행"하기로 확정한 사안이라 착수 전 범위 재확인 권장
- **자연어 조건 파싱 구현 (§8 다음 작업 1번, 사용자 승인)** — 사용자가 "AI Chat 1차 구현 범위에서 SQL 조회·권한 필터링·환각 방지까지 한 번에 포함하지 말자는 것이었을 뿐 영구 제외는 아니다"라고 명확히 하며 착수를 승인, 이번 작업 범위를 자연어 조건 파싱으로만 제한하도록 명시적으로 지시받아 그대로 진행. `backend/app/services/ai_parser.py`(신규) — LLM을 사용하지 않고 규칙 기반(마스터 데이터 매칭 + 정규식)으로만 파싱해 "LLM이 임의 SQL을 생성하지 않는다"는 원칙을 준수: `parse_query(db, message)`가 기존 repository(`codes.py`의 `list_job_types`/`list_departments`, `hr_skill_mst.py`의 `list_skills`)로 마스터 데이터를 조회해 직무 유형(`JIKMU_CD`/`JIKMU_NM`, 부기 코드 제거 매칭)·기술명(전체명 우선 매칭 후 토큰 단위 부분 매칭, 예: "Spring"→"Spring Boot")·부서명(`DEPT_NM` 부분 일치)을 매칭하고, 정규식으로 가동일/기간(오늘·즉시/이번 달/다음 달/다음 주/특정 월/특정 날짜 "YYYY-MM-DD"·"MM월DD일")과 최소 숙련도("숙련도 N 이상")를 추출. 표준으로 만들지 못한 조건(가동률 임계값 표현, "시니어" 등 연차/직급 뉘앙스, 매칭 실패한 영문 약어)은 버리지 않고 `unresolved_terms`에 원문 그대로 기록. `backend/app/schemas/ai_chat.py`에 `ParsedResourceQuery`(사용자 지정 JSON 형태와 동일한 필드: `intent`/`job_type`/`skills`/`min_proficiency_level`/`available_from`/`department`/`confidence`/`unresolved_terms`) 신규 추가. **SQL 조회는 이번 범위에서 수행하지 않음** — 마스터 데이터 조회(직무 유형/기술/부서 목록)만 기존 repository를 재사용했을 뿐, 리소스 검색 자체는 다음 작업으로 분리했고, `POST /api/v1/ai/chat`·`/ai-chat` 화면도 아직 이 파서를 호출하지 않는다(§11 AI Chat 체크리스트에 명시). 권한 필터링·환각 방지 프롬프트도 이번 범위에서 적용하지 않되, `ai_parser.py`를 `ai_chat.py`(LLM 호출)와 독립된 모듈로 분리해 다음 작업에서 파싱 결과를 SQL 조회에 넘기는 지점에 권한 필터링 레이어를 끼워 넣을 수 있도록 모듈 경계를 나눠뒀다(파일 상단 주석에 명시). `backend/tests/test_ai_parser.py`(신규) — 사용자가 제시한 10개 예시 질의(다음 달 Java 아키텍트, 8월 Spring 개발자, 개발1팀 Python, 이번 달 종료 예정자, 가동률 50% 이하 PM, K-ICS BA, PostgreSQL 백엔드 개발자, 즉시 투입 시니어 개발자, 다음 주 React 개발자, 보험 프로젝트 아키텍트) 전부와 숙련도 조건·완전 무관 질의(unknown intent) 2건을 추가해 총 12개 케이스 작성, 전부 통과. **실 서버 컨테이너에서 실제 pytest 실행으로 검증**(별도 DB 스키마 변경 없음, 기존 Alembic Seed의 `HR_JIKMU_MST`/`HR_SKILL_MST` 데이터를 그대로 활용): pytest 66→78개 전부 통과. Phase 6 진행률 38%→50%로 갱신(8개 항목 중 4개 완료), §3/§4/§9-1/§11 항목 갱신, §8 큐를 사용자가 이미 순차 진행을 확정한 "파싱 결과 → SQL 조회 → 결과 요약 흐름 구현"으로 재구성(착수 시 whitelist 기반 intent + 기존 repository/query builder만 사용, free-form SQL 생성·실행 금지 — 사용자 지침 유지)
- **파싱 결과 → SQL 조회 → 결과 요약 흐름 구현 (§8 다음 작업 1번)** — `backend/app/services/ai_resource_search.py`(신규) `search_resources(db, parsed)` — whitelist 원칙(사용자 지침) 그대로 준수: `ParsedResourceQuery.intent == "resource_search"`인 경우에만 §8 이전 작업에서 이미 구현한 `hr_avail_snap.list_availability`(직무 유형·부서·기술·숙련도 복합 필터)를 그대로 재사용해 조회하고, LLM은 이 조회 과정에 전혀 관여하지 않는다(SQL 신규 작성 없음). 직무 유형명/부서명/기술명을 각각 `JIKMU_ID`/`DEPT_ID`/`SKILL_ID`로 변환하는 조회는 기존 `codes.py`/`hr_skill_mst.py` repository를 그대로 사용. `available_from`이 파싱되면 `AVAIL_STAT_CD='AVAILABLE'`이거나 `AVAIL_STRT_DT`가 그 날짜 이전인 사원만 남기는 후처리 필터를 추가. **알려진 제약**: `list_availability`는 `skill_id` 하나만 받으므로 기술이 여러 개 파싱되면 첫 번째만 조회에 반영하고 나머지는 `skipped_skills`로 반환 — 응답 요약 문구에 "이 조건은 반영되지 않았다"고 안내(다중 기술 AND 조회는 후속 확장 대상, §9-1에 기록하지 않고 코드 주석으로만 명시할 만큼 경미한 제약으로 판단). `backend/app/repositories/hr_empl_mst.py`에 `list_employees_by_ids`(신규, ID 목록으로 사원 일괄 조회) 추가해 검색 결과에 사번/성명을 조인. `backend/app/schemas/ai_chat.py`에 `ResourceSearchItem`/`ResourceSearchResult` 스키마 신규 추가. `backend/app/api/v1/ai_chat.py`의 `POST /api/v1/ai/chat`을 갱신 — 메시지를 먼저 `parse_query`로 파싱해 `intent=="resource_search"`면 `search_resources` 결과 요약을 그대로 응답(LLM 미호출, 환각 위험 없음), 그 외(`intent=="unknown"`)는 기존 LLM 단순 호출 경로를 그대로 유지(회귀 없음 — 기존 `test_chat_returns_llm_reply` 등 5개 테스트가 수정 없이 그대로 통과함으로 확인). **권한 필터링·환각 방지 프롬프트는 이번 범위에서 구현하지 않음** — `search_resources`는 요청자 권한과 무관하게 전체 재직 사원을 대상으로 조회해, VIEWER 등 제한된 권한도 AI Chat을 통해 조직 전체 인력 정보를 열람할 수 있는 상태 그대로다(신규 리스크로 §9에 기록, 다음 §8 작업으로 연결). `backend/tests/test_ai_resource_search.py`(신규, 4개 케이스 — 직무 유형 매칭/무매칭 시 빈 요약/가동일 필터/다중 기술 skip)와 `test_ai_chat.py`에 1개 케이스(조건 인식 시 `call_llm` 미호출 검증) 추가. **실 서버 컨테이너에서 실제 pytest 실행으로 검증**(DB 스키마 변경 없음): pytest 78→83개 전부 통과. Phase 6 진행률 50%→63%로 갱신(8개 항목 중 5개 완료), §3/§4/§9/§9-1/§11 항목 갱신, §8 큐를 "권한 필터링 후 LLM 컨텍스트 전달 구현"으로 재구성
- **DB 목데이터(사원·프로젝트) 생성 스크립트 추가 (사용자 요청, §8 큐 항목 아님)** — `reference/ResourceManagement_v2.xlsx`(인력마스터_ResourceTable, 프로젝트투입_ProjectTable 시트)의 컬럼·값 형식(사번 `BW-NNN`, 팀 3종, 직급 10단계, 보유역할 복수, 휴대폰 `010-0000-0000`)을 그대로 따라 `backend/app/db/mock/load_mock_data.py`(신규)를 작성 — 사원 30명(부서 3종·직무유형 12종 전반에 분산, 보유역할·기술스택 2~4개씩 포함), 프로젝트 12건(고객사명은 실제 금융회사 명칭 — 신한은행/KB국민은행/하나은행/우리은행/NH농협은행/카카오뱅크/토스뱅크/삼성생명/교보생명/미래에셋증권/신한카드/현대카드, 단 프로젝트명·투입 내역은 전부 가상 예시), 투입 이력 30건(RUNNING/PLANNED/CLOSED/HOLD 프로젝트 상태와 ACTIVE/PLANNED/DONE 투입 상태를 골고루 포함해 가동 가능 인력 화면의 AVAILABLE/PARTIAL/FULL 3개 상태를 실제로 재현)을 생성. 공식 마스터 Seed(`backend/app/db/seed/`, Alembic 마이그레이션으로 관리)와 성격이 달라(스키마가 아닌 예시 트랜잭션 데이터) 별도 디렉토리(`app/db/mock/`)의 독립 실행 스크립트로 분리하고 Alembic에는 포함하지 않음 — `docker compose exec api python -m app.db.mock.load_mock_data`로 실행, `EMPL_NO`/`PJT_CD` 기준으로 이미 있는 행은 건너뛰어 재실행해도 안전(멱등성 확인 완료: 2회 연속 실행 시 2번째는 0건 생성). 검증 중 `search_resources`(직전 작업)가 마스터 데이터에 없는 부서/직무/기술 조건을 조용히 무시하고 전체 조회로 흘려보내던 잠재 버그(목데이터 투입 전에는 DB가 비어 있어 드러나지 않았음)를 발견해 함께 수정 — 조건이 마스터 데이터에서 ID로 변환되지 않으면 즉시 빈 결과를 반환하도록 방어 로직 추가. **실 서버 컨테이너에서 실제 스크립트 실행 및 psql로 검증**: 사원 30명/프로젝트 12건/투입 이력 30건 정상 반영 확인, 재실행 시 중복 생성 없음 확인. 이 수정으로 `backend/tests/test_ai_resource_search.py`의 무매칭 케이스가 실제 데이터 존재 시에도 정상 통과함을 확인, pytest 83개 전부 통과(신규 테스트 추가 없이 기존 회귀 통과만 재확인). 사원·프로젝트 목록 화면(`/employees`, `/projects`)은 여전히 프론트엔드 목데이터 기반이라(§9-1 기존 항목) 이번에 DB에 넣은 데이터가 화면에 바로 나타나지는 않음 — DB/API 레벨(`GET /api/v1/employees`, `/projects`, `/availability` 등)에서는 즉시 조회 가능. `.env`/DESIGN 파일은 수정하지 않음
- **사원 목록 화면(`/employees`) 실 API 연동 + 목데이터 정리 스크립트 추가 (사용자 요청)** — 위 항목에서 확인한 "DB에는 있으나 화면에는 안 보이는" 문제를 해소. **`/projects` 화면은 확인 결과 이미 실 API(`GET /api/v1/projects`) 연동 상태**였다(2026-07-04 이전 세션에서 완료, §9-1에 반영 누락되어 있었을 뿐 — 별도 작업 불필요). **`/employees` 화면만 실제로 `lib/mock-data.ts` 기반이라 전면 재작성**: `frontend/app/(app)/employees/page.tsx`가 `GET /api/v1/employees`+`departments`/`positions`/`job-types`/`availability`를 병렬 조회해 조인하도록 교체(다른 실 API 전환 화면들과 동일한 클라이언트 조인 패턴). 단 "보유 역할"(복수 `HR_EMPL_ROLE_REL`) 배지를 표시할 조회 API가 그동안 전혀 없었음을 발견 — `backend/app/repositories/hr_empl_role_rel.py`, `backend/app/api/v1/employee_roles.py`(`GET /api/v1/employee-roles`, 신규, 권한 `employees.view` 재사용, 등록/수정 API는 화면 요구사항이 없어 이번 범위에서 제외) 신규 작성해 연결. 조직/직급/직무 유형 필터도 하드코딩된 `lib/options.ts` 목록 대신 실 마스터 데이터(`departments`/`positions`/`job-types` 응답) 기준으로 동적 생성(기술/직무유형 관리 화면에서 이미 확립한 원칙과 동일 적용) — 재직 상태 필터는 DB CHECK 제약과 동일한 고정 열거값이라 하드코딩 유지. 기존 신/구 `JIKMU_CD` 별칭 매핑(`JIKMU_CD_ALIASES`, 목데이터 전용 임시 코드)은 실 데이터 전환으로 불필요해져 제거. **범위를 의도적으로 축소한 부분**: "사원 등록" 모달은 여전히 `POST /api/v1/employees` API에 연결되지 않은 UI 전용 스텁으로 남겨둠(§9-1 기존 항목, 이번 요청 범위 밖) — 등록 후 새로고침 시 실 데이터가 반영되므로 화면 자체는 정상 동작. `backend/tests/test_employee_roles.py`(신규, 2개 케이스) 작성, pytest 83→85개 전부 통과. **목데이터 정리 스크립트**: `backend/app/db/mock/remove_mock_data.py`(신규) — `load_mock_data.py`의 `EMPLOYEES`/`PROJECTS` 데이터 정의를 그대로 import해 접두사 추측이 아닌 "이 스크립트가 실제로 넣은 행"만 정확히 특정(`EMPL_NO`/`PJT_CD` 기준), 투입 이력→역할/기술 연결→사원→프로젝트 순으로 FK 의존관계에 맞춰 삭제. 부서(영업/세일즈파트너/딜리버리)는 목데이터 전용이 아니라 운영에서도 쓸 조직 마스터라 삭제 대상에서 제외(주석으로 사유 명시). `docker compose exec api python -m app.db.mock.remove_mock_data`로 실행, 재실행해도 안전. **실 서버 컨테이너에서 실제 실행으로 검증**: 제거 실행 후 `HR_EMPL_MST`/`PJT_MST` 0건, `HR_DEPT_MST` 3건(부서 보존) 확인 → 재실행 시 전부 0건(멱등성) 확인 → 다시 `load_mock_data` 실행해 원상 복구, pytest 85개 전부 통과 재확인. `/employees` 페이지 200 렌더링 확인. §4 Phase 4 "사원 목록 화면 구현" 항목 갱신, §9-1 "사원 목록 화면 실 API 미연동" 항목 해소 처리, §11 항목 완료 체크
- **사원 상세·리포트 화면 오류 수정 (사용자 요청)** — 사용자가 두 화면에서 오류가 있다고 보고해 재현·조사 후 수정. 서버 로그(200 OK만 기록)로는 드러나지 않는 프론트엔드 런타임 크래시였음을 확인 — 브라우저가 연결되어 있지 않아(`list_connected_browsers` 빈 배열) 시각적으로 재현하지 못하고, 코드 정적 분석 + 백엔드 응답 스키마 직접 대조로 원인을 특정했다. **1) 사원 상세 화면(`/employees/[id]`) 크래시**: `frontend/app/(app)/employees/[id]/page.tsx`가 `GET /api/v1/projects`를 `ProjectOut[]`(배열)로 잘못 타입 지정해 호출하고 있었으나, 실제 응답은 `{total, skip, limit, items}` 페이지네이션 객체(다른 화면들과 동일한 공통 스키마) — `projects.map(...)`이 배열이 아닌 객체에 호출되어 "사원 상세" 탭 전환 시마다(투입 이력 프로젝트명 조인 단계에서) `TypeError: projects.map is not a function`으로 크래시하고 있었음. `ProjectListResponse` 타입을 추가하고 `?limit=200`과 `.items`로 수정. **2) 리포트 화면(`/reports`) 크래시**: `frontend/app/(app)/reports/page.tsx`의 "직무 미등록" `StatCard`가 `tone="danger"`를 사용했으나, `components/common/stat-card.tsx`의 `StatCardProps.tone`에는 `danger`가 정의되어 있지 않아 `toneStyles["danger"]`가 `undefined`를 반환 → 곧바로 `t.bg`/`t.fg`를 읽으며 `TypeError: Cannot read properties of undefined`로 크래시. `frontend/next.config.mjs`에 `typescript.ignoreBuildErrors: true`가 설정되어 있어 이런 타입 오류가 빌드 시점에 잡히지 않고 런타임까지 조용히 통과하고 있었음(다른 화면에 동일 패턴 없는지 전수 검색 완료 — `tone=`/`variant=` 값 전수 대조, 이 1건만 발견). `StatCard`에 `danger` 톤 스타일(Badge의 `danger` 변형과 동일한 배색)을 정식 추가해 해결 — 톤을 다른 값으로 바꿔 증상만 가리지 않고 실제로 지원되도록 함. **실 서버 컨테이너에서 재빌드 후 백엔드 응답 스키마와 프론트엔드 타입 일치 여부를 curl로 직접 대조해 검증**(`GET /projects` 실제 응답이 `{total,...,items}`임을 확인), pytest 85개 전부 통과(백엔드 변경 없음), `/employees/{id}`·`/reports` 페이지 200 렌더링 확인. `.env`/DESIGN 파일은 수정하지 않음
- **리포트 화면 탭 순서 변경 + "월별 가동률 통계" 매트릭스 실 구현 (사용자 요청)** — 탭 순서를 "주간/월간/매트릭스"에서 "매트릭스/주간/월간"으로 변경(초기 선택 탭도 매트릭스로 전환). 이전에 구조 복잡도로 후속 작업 분리해뒀던(§9-1) 매트릭스 탭을 이번에 실제로 구현 — 설계서(SCR-013 탭 3, `ResourceManagement_v2.xlsx` "가동률_통계" 시트) 그대로 반영. `backend/app/repositories/reports.py`에 `build_utilization_matrix(db, from_dt, to_dt, dept_id)` 신규 추가 — `PJT_ASGN_HIS`를 (사원, 프로젝트, 투입유형) 단위로 묶어 지정 기간의 각 월과 시작/종료일 겹침 여부로 월별 투입률을 재계산(과거 스냅샷을 보관하지 않는 기존 리포트 제약과 동일한 접근), 사원별 소계·연평균·100% 초과 월 목록과 조직 평균 3단계(수행중만/수행중+투입준비중/전체)를 산출. `backend/app/schemas/reports.py`에 `UtilizationMatrixRow`/`UtilizationMatrixEmployee`/`UtilizationMatrixOrgAvg`/`UtilizationMatrixOut` 신규 추가(설계서 JSON 응답 구조 그대로), `backend/app/api/v1/reports.py`에 `GET /reports/utilization-matrix?from={YYYYMM}&to={YYYYMM}&dept_id={id}` 신규 추가(권한은 기존 `reports.view` 재사용, `to<from`이면 422). 프론트엔드는 기존에 목데이터로만 존재하던 프로토타입 컴포넌트(`components/reports/utilization-matrix.tsx`, 히트맵 셀 스타일)를 실 API 데이터 소스로 교체 — 기간(월 범위 선택기, 기본값 최근 12개월)·부서 필터 추가, 프로젝트 유형 아이콘(🔵/🟠/🟢)·사원별 소계 행·100% 초과 강조(⚠)·조직 평균 3행 푸터까지 설계서 레이아웃대로 구현. Excel 내보내기·리포트 발송은 이번 범위에서도 제외(§9-1 유지). **실 서버 컨테이너에서 실제 HTTP 호출 및 임시 데이터로 검증**: 정상 투입 이력 반영 확인, API가 거부하는 100% 초과 조합을 DB에 직접 넣어(레거시 데이터 정합성 위반 재현) 초과 강조가 정확히 동작함을 확인, `from`/`to` 역순 422 확인. 현재 DB에 있는 목데이터(사원 30명·프로젝트 12건) 기준 최근 12개월 조회 결과 curl로 직접 확인 — 조직 평균 가동률이 16.7%→73.3%로 상승하는 추세가 실제 투입 이력과 일치함을 확인. `backend/tests/test_reports.py`에 3개 케이스 추가(pytest 85→88개 전부 통과). `/reports` 페이지 200 렌더링 확인
- **사이드바·톱내비 로고 교체 (사용자 요청)** — 사이드바 상단의 아이콘+"HRM 자동화/Resource Mgmt" 텍스트를 제거하고 그 자리에 사용자가 제공한 `Blueward-CI_Inverse.png`(150×27px, `next/image`)를 배치. 톱내비의 "전역 검색" 입력창(연동된 검색 기능이 없던 자리표시자)을 제거하고 그 자리에는 **사이드바에서 방금 제거한 기존 아이콘 로고**(흰색 배경의 `Boxes` 아이콘 박스) + "HRM 자동화 시스템(Resource Mgmt)" 텍스트를 옮겨 배치했다(최초 구현 시 CI 이미지를 두 곳 모두에 넣었다가, 사용자가 톱내비 쪽은 기존 사이드바 아이콘을 의미한 것이었다고 정정해 수정). 이미지 파일은 Next.js 정적 자산 서빙 규칙에 따라 `frontend/public/`로 위치시킴(`next/image` src는 `public/` 기준 절대 경로만 허용). 재빌드 후 이미지 200 서빙 확인, `/dashboard` 페이지 200 렌더링 확인, 백엔드 변경 없어 pytest 88개 그대로 통과
- **인력·투입 목데이터 조정 (사용자 요청)** — `backend/app/db/mock/load_mock_data.py`의 `EMPLOYEES`/`PROJECTS`/`ASSIGNMENTS` 정의를 조정. **1) 조직 구성**: "영업" 소속이던 5명 중 3명(21·22·23번, PM 역할)을 "세일즈파트너"로 이동해 "영업"에 2명(24·25번)만 남김 — 부서 자체는 삭제하지 않고 소속 인원만 재배치. **2) 잔류 2명 가동률 0%**: 24·25번의 기존 투입 이력(각각 50%/100%)을 전부 제거해 투입 이력이 아예 없는 상태(`list_availability` 기준 `TOT_ALLOC_RT=0`, `AVAIL_STAT_CD=AVAILABLE`)로 조정. **3) 연간 프로젝트 로테이션**: 2·9·18번 사원을 2025-01-01~12-31 A프로젝트(`PJT-2025-001`, 신한은행 코어뱅킹, `ASGN_STAT_CD=DONE`으로 종료 처리) → 2026-01-01~12-31 각기 다른 프로젝트(`ASGN_STAT_CD=ACTIVE`)로 재배치(A프로젝트 `STRT_DT`를 2025-01-01로 함께 조정해 투입 시작일과 정합). **4) 100% 초과 배정**: 11·12·13·14번 사원에 각 3~5개월(11번 3개월/12번 4개월/13번 5개월/14번 3개월) 겹치는 2건의 투입을 추가해 합계 120%가 되도록 조정 — `POST /assignments`는 100% 초과를 거부하므로 이 조합은 스크립트에서 ORM으로 직접 생성(레거시 데이터 정합성 위반 재현 목적, 기존 패턴과 동일). 조정 과정에서 원래 20·29번 사원의 기존 투입 이력을 실수로 함께 삭제했던 것을 재검토 중 발견해 즉시 복원. **실 서버 컨테이너에서 `remove_mock_data`→`load_mock_data` 재실행 후 실제 조회로 검증**: `HR_DEPT_MST` 부서별 인원수(영업 2/세일즈파트너 8/딜리버리 20) 확인, 24·25번 `GET /availability` 응답이 `TOT_ALLOC_RT=0`·`AVAILABLE`임을 확인, `GET /reports/utilization-matrix`로 11·12·13·14번이 지정한 개월 수만큼 정확히 120%·`over_100_months`에 표시됨을 확인, 2·9·18번이 2025년 A프로젝트→2026년 각기 다른 프로젝트로 월별 전환됨을 확인. 백엔드 코드 변경 없이 데이터만 조정한 작업이라 pytest 88개 그대로 통과(회귀 없음)
- **월별 가동률 통계 표 — 사원 정보 셀 병합 (사용자 요청)** — `components/reports/utilization-matrix.tsx`의 표를 "사원"/"프로젝트" 2개 컬럼으로 분리하고, "사원"(사번·성명·조직) 정보는 사원별 그룹의 첫 행에만 `rowSpan`으로 병합 표시하도록 변경(그동안은 프로젝트 행마다 사번·성명·조직·프로젝트명이 한 셀에 전부 반복 표시되고 있었음). 사용자가 제시한 표 형식(사원 열은 1회만, 이하 프로젝트 행은 빈칸)에 맞춰 반영. 좌측 고정(sticky) 컬럼은 "사원" 1개만 유지 — "프로젝트" 컬럼까지 sticky로 두면 실제 렌더링 너비에 따라 겹침이 발생할 수 있어 제외. 재빌드 후 `/reports` 페이지 200 렌더링 확인, 백엔드 변경 없어 pytest 88개 그대로 통과
- **권한 필터링 후 LLM 컨텍스트 전달 구현 (§8 다음 작업 1번)** — `search_resources`(직전 작업에서 구현)가 반환하는 데이터가 실질적으로 SCR-010 "가동 가능 인력" 화면 데이터와 동일함에 착안해, `POST /api/v1/ai/chat`이 `intent="resource_search"` 응답을 반환하기 전 요청자의 `SYS_ROLE_MST.PERM_JSON`에 `availability.view` 권한이 있는지 추가로 확인하도록 수정 — 권한이 없으면 `search_resources`를 아예 실행하지 않고 "가동 인력 상세 조회 권한이 없습니다..." 안내 메시지만 반환한다. `app/api/deps.py`에 `has_permission(db, current_user, screen, action) -> bool` 유틸을 신규 추가해 기존 `require_permission`(403 예외 발생형 의존성)과 동일한 `PERM_JSON` 조회 로직을 공유하도록 리팩터링(로직 중복 없음, 기존 `require_permission` 동작은 변경 없음 — `has_permission`을 내부에서 호출하도록만 바꿈). `backend/app/api/v1/ai_chat.py`의 `post_ai_chat`이 `require_permission("ai_chat","view")`을 파라미터 의존성으로 받아 `current_user`를 확보하도록 변경(기존에는 데코레이터 `dependencies=[]`로만 선언되어 반환값을 버리고 있었음 — 중복 호출 방지를 위해 데코레이터 쪽은 제거). **범위를 의도적으로 축소한 부분**: 설계서/사용자 요청이 언급한 "부서 범위"까지의 행(row) 단위 세부 제한(예: "본인 부서 인력만 조회 가능")은 이 프로젝트의 권한 모델(`require_permission`)이 애초에 화면×버튼 단위만 표현하고 행 단위 스코프는 다루지 않는다고 이미 문서화되어 있어(`app/api/deps.py` 기존 주석) 이번 범위에서도 동일하게 제외 — 화면(screen) 단위 권한(요청자가 SCR-010 화면 자체에 접근 가능한지)까지만 확인한다. `backend/tests/test_ai_chat.py`에 VIEWER가 resource_search 질의 시 차단되고(LLM도 호출되지 않음) 안내 메시지를 받는지 검증하는 케이스 1개 추가 — 기존 admin 대상 케이스(`test_chat_resource_search_intent_bypasses_llm`)가 수정 없이 그대로 통과함으로써 권한 있는 역할의 정상 동작도 함께 재확인됨. **실 서버 컨테이너에서 실제 pytest 실행으로 검증**(VIEWER/ADMIN 두 역할 모두 실제 JWT 토큰 발급 후 HTTP 요청): pytest 88개 전부 통과(신규 1건 포함). Phase 6 진행률 63%→75%로 갱신(8개 항목 중 6개 완료), §3/§4/§9/§9-1/§11 항목 갱신(§9 리스크 "AI Chat resource_search 조회 결과에 권한 필터링 미적용" 해소 처리), §8 큐를 "환각 방지 시스템 프롬프트 적용"으로 재구성
- **환각 방지 시스템 프롬프트 적용 (§8 다음 작업 1번)** — `app/services/ai_chat.py`의 `call_llm`(DB 조회 없이 응답하는 `intent="unknown"` 자유 대화 경로 전용, `resource_search`는 이 함수를 아예 호출하지 않아 대상 아님)이 매 호출마다 시스템 메시지로 환각 방지 프롬프트(`_ANTI_HALLUCINATION_SYSTEM_PROMPT`)를 함께 전달하도록 수정 — 실존 여부를 확인할 수 없는 사원명·사번·프로젝트명·투입률·가동일·조직 배치 등 구체적인 HR 데이터를 지어내지 말고, 특정 인력 검색·추천·가동 현황 질의에는 답을 지어내는 대신 시스템의 조건 기반 조회 기능(직무 유형·기술·가동 가능일 포함)을 이용하도록 안내하라는 지침, 확실하지 않은 내용은 모른다고 밝히도록 명시. OpenAI 호환 `chat/completions` API의 `messages` 배열에 `{"role":"system", ...}`을 `{"role":"user", ...}` 앞에 추가하는 방식으로 구현(DeepSeek 포함 대부분의 LLM 공급자가 지원하는 표준 방식). `backend/tests/test_ai_chat_service.py`(신규) — `httpx.post`를 모킹해 실제 네트워크 호출 없이 요청 페이로드에 시스템 메시지가 포함되고 그 내용에 금지 지침이 담겨 있는지 검증(1개 케이스). **실 서버 컨테이너에서 실제 pytest 실행으로 검증**: pytest 88→90개 전부 통과. Phase 6 진행률 75%→88%로 갱신(8개 항목 중 7개 완료 — 남은 항목은 "테스트 질의 10개 이상 검증" 하나뿐), §3/§4/§9-1/§11 항목 갱신, §8 큐를 "테스트 질의 10개 이상 검증"으로 재구성(완료되면 Phase 6가 100%가 됨)
- **테스트 질의 10개 이상 검증 (§8 다음 작업 1번) — Phase 6 완료** — `ai_parser.py`의 기존 12개 파싱 단위 테스트와 별개로, 설계서가 요구하는 "엔드투엔드 질의 검증"을 위해 `backend/tests/test_ai_chat_e2e.py`(신규) 작성 — 사용자가 자연어 조건 파싱 작업 당시 직접 제시했던 예시 질의 10개(직무 유형·기술·부서·가동일 조건 각각 포함: "다음 달 투입 가능한 Java 아키텍트", "8월 Spring 개발자", "개발1팀 Python", "이번 달 종료 예정자", "가동률 50% 이하 PM", "K-ICS BA", "PostgreSQL 백엔드 개발자", "즉시 투입 시니어 개발자", "다음 주 React 개발자", "보험 프로젝트 아키텍트")를 `POST /api/v1/ai/chat` 실제 엔드포인트로 호출해 `call_llm`이 전혀 호출되지 않는지(=파싱→권한 확인→조회 전체 경로가 정상적으로 resource_search로 인식했는지) 검증. 일반 대화("안녕하세요 반갑습니다")는 반대로 LLM 경로로 정상 폴백되는지 확인하는 회귀 케이스 1건도 함께 추가(총 11개 케이스). **검증 중 표기 오류 발견 및 수정**: 실제 목데이터로 curl 검증하는 과정에서 `search_resources`의 응답 요약 문구가 "가동률 {AVAIL_RT}%"라고 표시하고 있었으나, `AVAIL_RT`는 실제로 "가동 가능률"(100-투입률)이라 의미가 정반대로 읽히는 문제를 발견 — "가동 가능률"로 표기를 수정(`backend/app/services/ai_resource_search.py`). **실 서버 컨테이너에서 실제 pytest 실행 및 curl로 실제 목데이터 대상 재현·검증**: pytest 90→101개 전부 통과, curl로 "즉시 투입 가능한 시니어 개발자" 질의 시 실제 사원 2명이 올바른 문구로 반환됨을 확인. Phase 6 진행률 88%→100%로 갱신(8개 항목 전부 완료, 개발 상태 "진행 중→완료"로 전환), §3/§4/§5/§11 항목 갱신, §8 큐를 §3/§4 로드맵상 다음 순서인 Phase 7(운영 자동화 및 배포 안정화, 0%)의 첫 항목 "`HR_AVAIL_SNAP_GEN` 배치 구현"으로 재구성 — 이 배치가 완성되면 Phase 5의 마지막 잔여 항목("가동 가능일 자동 계산 로직 구현")도 함께 해소 가능
- **`HR_AVAIL_SNAP_GEN` 배치 구현 (§8 다음 작업 1번)** — 설계서 §10.1·산출물(`worker.py`)이 요구하는 배치 스케줄러 방식(APScheduler)으로 구현. `backend/app/repositories/hr_avail_snap.py`에 `generate_avail_snap(db, snap_dt)` 신규 추가 — 기존 화면용 `list_availability`(재직 사원 전체 가동률 즉시 계산)를 그대로 재사용하고, 계산 결과를 `HR_AVAIL_SNAP` 테이블에 스냅샷 행으로 저장(같은 날짜로 재실행해도 안전하도록 저장 전 해당 날짜 기존 스냅샷을 먼저 삭제 후 재삽입). `backend/app/services/avail_snap_gen.py`(신규) `run_avail_snap_gen`이 배치 실행을 감싸 성공/실패 여부와 무관하게 `SYS_BATCH_HIS`에 실행 이력(시작/종료 시각, 생성 건수, 실패 시 에러 메시지)을 기록 — 배치가 예외로 죽어도 이력이 남아야 운영팀이 미실행을 감지할 수 있다는 원칙 적용. `backend/app/worker.py`(그동안 `print` 자리표시자였음)를 APScheduler `BlockingScheduler`로 교체해 매일 KST 01:00에 이 배치를 실행하도록 등록(`docker-compose.yml`의 기존 `worker` 서비스, `restart: unless-stopped`가 이미 구성되어 있어 컨테이너 설정 변경 없이 실행 파일만 교체). `requirements.txt`에 `apscheduler==3.10.4` 추가. **실 서버 컨테이너에서 실제 실행으로 검증**: `worker` 컨테이너 재빌드 후 로그로 스케줄러 정상 기동 및 작업 등록 확인, 배치 함수를 수동 실행해 현재 DB 목데이터(재직 사원 30명) 기준 `HR_AVAIL_SNAP`에 스냅샷 30건(AVAILABLE 10/PARTIAL 3/FULL 17) 정상 생성 및 `SYS_BATCH_HIS`에 `SUCCESS` 이력 기록 확인, 동일 날짜로 재실행해도 30건 그대로 유지되어 멱등성 확인. `backend/tests/test_avail_snap_gen.py`(신규, 2개 케이스 — 스냅샷·배치 이력 생성 확인, 동일 날짜 재실행 시 중복 없음) 작성, pytest 101→103개 전부 통과. **범위를 의도적으로 축소한 부분**: 대시보드(`dashboard.py`)·리포트(`reports.py`) API는 여전히 이 스냅샷 테이블을 조회하지 않고 매 요청 실시간 재계산 방식을 그대로 사용한다(§9 기존 리스크 2건과 동일 — 이번 배치 신규 구현이 그 리스크를 자동으로 해소하지는 않음, 스냅샷 기반 조회로 전환하는 것은 별도 후속 작업). Phase 5 마지막 항목("가동 가능일 자동 계산 로직 구현")도 함께 완료 처리되어 Phase 5 진행률 88%→100%(개발 상태 "진행 중→완료"), Phase 7 진행률 0%→10%(개발 상태 "예정→진행 중"), §3/§4/§5/§9-1/§11 항목 갱신, §8 큐를 Phase 7 다음 순서 "`PJT_ASGN_END_ALERT` 배치 구현"으로 재구성
- **`PJT_ASGN_END_ALERT` 배치 구현 (§8 다음 작업 1번)** — `backend/app/repositories/pjt_asgn_his.py`에 `list_ending_soon_assignments(db, as_of, within_days=30)` 신규 추가 — `ASGN_STAT_CD='ACTIVE'`이고 `ASGN_END_DT`가 기준일로부터 30일 이내(종료일 미정 건은 "종료 예정"이 아니므로 제외)인 투입 건을 사원/프로젝트명과 함께 조회. `backend/app/services/teams_notify.py`(신규) `send_teams_message`가 `TEAMS_WEBHOOK_URL` 설정 여부에 따라 분기 — 미설정 시 예외 없이 `False`를 반환하고 조용히 건너뛴다(AI Chat의 `DEEPSEEK_API_KEY` 미설정 처리와 동일한 선택적 연동 패턴), URL은 있으나 전송 자체가 실패한 경우만 예외. `backend/app/services/asgn_end_alert.py`(신규) `run_asgn_end_alert`가 조회→메시지 구성→Teams 전송 시도→`SYS_BATCH_HIS` 이력 기록까지 담당(`HR_AVAIL_SNAP_GEN`과 동일한 성공/실패 무관 이력 기록 원칙). `backend/app/core/config.py`에 `TEAMS_WEBHOOK_URL` 필드 신규 추가(`.env.example`에는 이미 있던 항목, `.env` 자체는 수정하지 않음). `backend/app/worker.py`에 매주 금요일 17:00(KST) cron 작업으로 등록(`HR_AVAIL_SNAP_GEN`과 함께 두 번째 등록 작업). **실 서버 컨테이너에서 실제 실행으로 검증**: `worker` 재빌드 후 로그로 두 작업 모두 정상 등록 확인, 배치 함수를 수동 실행해 현재 DB 목데이터 기준 종료 예정 1건을 정확히 찾아내고 `SYS_BATCH_HIS`에 `SUCCESS` 이력(및 "TEAMS_WEBHOOK_URL 미설정 — 알림 전송 생략" 문구) 기록 확인. **검증 중 테스트 설계 이슈 발견 및 수정**: 처음에는 절대 건수(`CRT_CNT == N`)로 단정하는 테스트를 작성했으나, 실 DB에는 이미 목데이터 투입 이력이 커밋되어 있어(별도 테스트 트랜잭션 격리 밖의 영구 데이터) 배치가 스캔하는 `PJT_ASGN_HIS` 전체 테이블과 섞여 절대값 비교가 신뢰할 수 없음을 발견 — 다른 리포트 테스트에서 이미 쓰인 "실행 전/후 비교" 패턴으로 전환해 해결. `backend/tests/test_asgn_end_alert.py`(신규, 2개 케이스) 작성, pytest 103→105개 전부 통과. **알려진 한계**: `TEAMS_WEBHOOK_URL`이 `.env`에 미설정 상태라 실제 Teams 채널로의 알림 발송 자체는 검증하지 못함 — 배치 로직과 이력 기록은 정상 동작 확인(§9 리스크로 기록, 운영팀이 웹훅 URL을 `.env`에 설정하면 코드 변경 없이 자동으로 실제 전송 경로를 탄다). Phase 7 진행률 10%→20%로 갱신, §4/§5/§9/§11 항목 갱신, §8 큐를 Phase 7 다음 순서 "`HR_DATA_QUALITY_CHK` 배치 구현"으로 재구성
- **사원 목록 "사원 등록" 모달 API 연동 (§9-1 첫 번째 미완료 항목, 사용자 지시)** — 이번 턴은 §8 큐가 아니라 §9-1 "완료 표시된 화면의 미구현 세부 기능" 체크리스트를 문서 순서대로 처리하라는 사용자 지시에 따라 진행. 목록 최상단 미완료 항목인 "사원 등록 모달 — `POST /api/v1/employees` 미연결"을 처리. `frontend/components/employees/employee-form-modal.tsx`를 실 API 연동으로 전면 재작성 — 그동안 목데이터(`Employee` 타입, `lib/options.ts`의 하드코딩된 `teamOptions`/`positionOptions`)를 사용하던 조직/직급 Select를 부모(`employees/page.tsx`)가 이미 조회해둔 실 마스터 데이터(`departments`/`positions`, `DEPT_ID`/`JIKGUP_ID`)를 props로 전달받아 사용하도록 교체(신규 fetch 없이 재사용, 다른 화면들과 동일한 원칙). `onSubmit`을 `POST /api/v1/employees` 실 호출로 교체(`ApiError` 메시지를 폼에 그대로 노출, 예: 사번 중복 409), 등록 성공 시 `onSaved` 콜백으로 부모의 `reload()`를 호출해 목록을 즉시 갱신하도록 연결(`employees/page.tsx`도 함께 수정). **범위를 의도적으로 축소한 부분**: 수정(edit) 모드는 이번 범위에서 제외 — 사원 상세 화면에 "정보수정" 버튼/폼 자체가 아직 없어(§9-1 별도 항목) 이 모달을 편집 용도로 열 진입점이 없기 때문. 기존에 있던 미사용 `employee`/`isEdit` prop(목데이터 타입 기준이라 실 API와 필드가 맞지 않음)은 제거하고, 그 작업 착수 시 `PATCH /api/v1/employees/{empl_id}`와 함께 다시 추가하도록 주석으로 명시. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 실제 부서/직급 ID로 curl `POST /api/v1/employees` 호출해 정상 등록(201) 확인, 검증에 사용한 임시 사원은 SQL로 삭제. `/employees` 페이지 200 렌더링 확인. 백엔드 API는 기존 것을 그대로 사용해 코드 변경이 없어 pytest 105개 그대로 통과. §9-1 "사원 목록 '사원 등록' 모달" 항목 해소 처리
- **사원 상세 화면 정보수정 버튼/폼 구현 (§9-1 다음 미완료 항목)** — 지난 턴에 제거했던 `employee` prop을 예고한 대로 `employee-form-modal.tsx`에 다시 추가해 수정 모드를 구현: `employee` prop이 전달되면(사원 상세 화면에서) 그 값으로 폼을 초기화하고 `PATCH /api/v1/employees/{empl_id}`를 호출, 전달되지 않으면(사원 목록의 "사원 등록" 버튼) 기존과 동일하게 `POST`로 등록 — 하나의 컴포넌트로 등록/수정 두 화면을 모두 지원(기존 프로젝트 관례상 재사용 가능한 위치를 우선 확인한 결과). 수정 모드에서는 사번(`EMPL_NO`) 입력을 비활성화(등록 후 변경 불가 원칙 유지). `frontend/app/(app)/employees/[id]/page.tsx`에 "정보수정" 버튼 추가(그동안 "편집 폼 UI 없음"이라 조회 전용이었던 자리) — `loadEmployeeDetail`이 이미 병렬 조회하던 `departments`/`positions` 배열을 반환값에 포함하도록 확장해(신규 API 호출 없이 재사용) 모달의 조직/직급 Select에 그대로 전달, 저장 성공 시 상세 화면 데이터를 재조회(`reload`)해 최신 정보를 즉시 반영. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 curl로 `PATCH /api/v1/employees/{empl_id}`(연락처 변경) 호출해 정상 반영 확인, 검증 직후 원래 값으로 복원. `/employees/{empl_id}` 페이지 200 렌더링 확인. 백엔드 API는 기존 것을 그대로 사용해 코드 변경이 없어 pytest 105개 그대로 통과. §9-1 "사원 상세 화면 정보수정 버튼/폼" 항목 해소 처리
- **사원 상세 화면 기술추가 버튼/폼 구현 (§9-1 다음 미완료 항목)** — `frontend/components/employees/employee-skill-form-modal.tsx`(신규) 작성 — 백엔드 `POST /api/v1/employee-skills`는 이미 구현되어 있어 프론트엔드 폼만 신규 추가. 기술 Select는 사원 상세 화면이 이미 조회해둔 전체 기술 목록(`loadEmployeeDetail`의 `skills` 변수, 반환값에 `skillCatalog`로 추가 노출해 신규 API 호출 없이 재사용)에서 해당 사원이 이미 보유한 기술(`ownedSkillIds`)을 제외한 목록만 노출해 중복 등록(백엔드 409) 자체를 사전에 방지. 숙련도(1~5 Select), 경력(년, 선택), 최근 사용일(선택) 입력 지원. `employees/[id]/page.tsx`의 "보유 기술" 탭 헤더에 "기술 추가" 버튼 추가, 저장 성공 시 상세 데이터 재조회(`reload`). **범위를 의도적으로 축소한 부분**: 이미 등록된 기술 항목의 수정(`PATCH /api/v1/employee-skills/{id}`, 예: 숙련도 변경)은 이번 범위에서 다루지 않음 — 별도 후속 작업으로 분리. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 curl로 `POST /api/v1/employee-skills` 호출해 정상 등록(201) 확인, 검증에 사용한 임시 사원-기술 연결은 SQL로 삭제. `/employees/{empl_id}` 페이지 200 렌더링 확인. 백엔드 API는 기존 것을 그대로 사용해 코드 변경이 없어 pytest 105개 그대로 통과. §9-1 "사원 상세 화면 기술추가 버튼/폼" 항목 해소 처리
- **사원 등록·수정 화면에서 "직무 유형" 지정 가능하도록 개선 (사용자 직접 요청)** — 사용자가 "사원정보 중 직무 유형을 수정하려면 어떻게 해야 해?"라고 질문해, 백엔드 `EmployeeCreate`/`EmployeeUpdate` 스키마는 이미 `JIKMU_ID`를 지원하지만 등록/수정 공용 모달(`employee-form-modal.tsx`)에는 해당 입력 필드 자체가 없어 UI로는 지정할 방법이 없음을 확인해 답변, 이어 "지정할 수 잇게 고쳐줘" 지시에 따라 프론트엔드만 수정. `employee-form-modal.tsx`에 "직무 유형" Select 필드 추가(호출부가 이미 조회해둔 `job-types` 마스터 데이터를 `jobTypes` prop으로 전달받아 재사용, 다른 마스터 데이터 Select와 동일한 원칙) — "선택 안 함" 옵션 선택 시 `JIKMU_ID: null`로 저장 가능. `employees/page.tsx`("사원 등록" 모달)는 이미 조회해둔 `jobTypes` state를 그대로 전달, `employees/[id]/page.tsx`("정보수정" 모달)는 `loadEmployeeDetail`이 `jobTypeName` 계산을 위해 이미 조회해두고도 반환값에 노출하지 않던 `jobTypes` 배열을 `EmployeeDetailData`에 추가 노출해 신규 API 호출 없이 재사용. 백엔드 변경 없음, pytest 105개 그대로 통과. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 curl로 `PATCH /api/v1/employees/{empl_id}`에 `JIKMU_ID` 전달 시 정상 반영 확인, 검증 직후 원래 값으로 복원. `/employees`, `/employees/{empl_id}` 페이지 200 렌더링 확인. §9-1 정식 체크리스트 항목이 아닌 사용자 직접 요청 건으로 별도 체크 항목 변경 없음
- **사원 상세 화면 퇴직처리 버튼 구현 (§9-1 다음 미완료 항목)** — 목록 순서상 다음 미완료 항목인 "사원 상세 화면 — 퇴직처리 버튼 없음"을 처리. 백엔드 `DELETE /api/v1/employees/{empl_id}`(로우 삭제가 아니라 `EMPL_STAT_CD='RETIRED'` 전환 + `RETIR_DT` 기록하는 소프트 삭제)는 이미 구현되어 있어 프론트엔드 연동만 추가. `frontend/lib/api.ts`에 `apiDelete` 헬퍼 신규 추가(기존 `apiGet`/`apiPost`/`apiPatch`와 동일한 에러 처리 패턴). 그동안 어느 화면에서도 실제로 연결되지 않고 있던 기존 공용 컴포넌트 `frontend/components/common/confirm-dialog.tsx`(`ConfirmDialog`)를 처음으로 사용 — 사원 상세 화면(`employees/[id]/page.tsx`)의 "정보수정" 버튼 옆에 "퇴직처리" 버튼을 추가하고, 클릭 시 확인 다이얼로그(파괴적 동작이므로 `destructive` 스타일)를 거쳐 `DELETE` 호출, 이미 퇴직 처리된 사원(`EMPL_STAT_CD==='RETIRED'`)은 버튼을 비활성화해 중복 요청(백엔드 409) 자체를 UI에서 방지, 처리 성공 시 상세 데이터 재조회(`reload`)로 상태 배지 즉시 반영. 백엔드 변경 없음, pytest 106개 그대로 통과. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 임시 사원 1명을 생성해 curl로 `DELETE` 호출 시 `EMPL_STAT_CD`가 `ACTIVE→RETIRED`, `RETIR_DT`가 오늘 날짜로 정상 전환됨을 확인, 동일 사원 재차 `DELETE` 시 409 확인, 검증에 사용한 임시 사원은 SQL로 삭제. `/employees` 페이지 200 렌더링 확인. §9-1 "사원 상세 화면 퇴직처리 버튼" 항목 및 관련 §9 리스크(정보수정·기술추가·퇴직처리 UI 미구현) "해소" 처리
- **사원 상세 화면 "변경 이력" 탭 구현 (§9-1 다음 미완료 항목)** — 목록 순서상 다음 미완료 항목인 "사원 상세 화면 '변경 이력' 탭 — `tgt_id` 단건 필터 미지원 + 화면 탭 UI 미연동"을 처리. 백엔드 `backend/app/repositories/sys_audit_log.py`의 `list_audit_logs`와 `backend/app/api/v1/audit_logs.py`의 `GET /audit-logs`에 `tgt_id`(UUID) 쿼리 파라미터 신규 추가 — 기존 `tgt_tbl_nm`과 함께 지정하면 특정 대상 1건의 변경 이력만 조회 가능(모델의 `TGT_ID` 컬럼은 이미 존재해 스키마 변경 불필요). 프론트엔드 `employees/[id]/page.tsx`에 "변경 이력" 탭을 추가하고 `GET /api/v1/audit-logs?tgt_tbl_nm=HR_EMPL_MST&tgt_id={empl_id}` 호출로 연동 — `settings_audit_logs.view` 권한이 Admin 전용(SCR-016 설계 원칙)이라 일반 사용자·HR_MGR가 사원 상세 화면 자체는 볼 수 있어도 이 탭에서는 403을 받을 수 있으므로, 탭을 클릭할 때만 지연 조회하고 403은 별도로 감지해 화면 전체 에러가 아니라 탭 내부에 "변경 이력 조회 권한이 없습니다" 안내만 표시하도록 처리(권한 정책은 그대로 유지, UX만 개선). 표시 컬럼은 시각/작업/수행자로 최소화(BFR/AFT_VAL_JSON 상세는 이미 설정 화면의 감사 로그 탭이 제공하므로 중복 구현하지 않음). `backend/tests/test_audit_logs.py`에 `tgt_id` 필터 회귀 테스트 1건 추가, pytest 106→107개 전부 통과. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 curl로 `GET /audit-logs?tgt_tbl_nm=HR_EMPL_MST&tgt_id={empl_id}` 호출 시 해당 사원의 로그만 반환됨을 확인(다른 사원 데이터와 섞이지 않음), `/employees/{empl_id}` 페이지 200 렌더링 확인. §9-1 "사원 상세 화면 변경 이력 탭" 항목 및 관련 §9 리스크(감사 로그 조회 API 부재) "해소" 처리
- **프로젝트 상세 화면 수정 버튼/폼 구현 (§9-1 다음 미완료 항목)** — 목록 순서상 다음 미완료 항목인 "프로젝트 상세 화면 — 수정 버튼/폼 없음"을 처리. 백엔드 `PATCH /api/v1/projects/{pjt_id}`는 이미 구현되어 있어 프론트엔드 연동만 추가. 그동안 프로젝트 목록 화면(`projects/page.tsx`)에 인라인 함수로만 존재하던 등록 전용 모달을, 이미 저장소에 있었으나 목데이터 기반(`onSubmit` 시 실제 저장 없이 폼만 초기화)이라 어디에서도 실제로 쓰이지 않던 `frontend/components/projects/project-form-modal.tsx`를 실 API 연동 공용 컴포넌트로 교체하며 그 자리에 추출 — 사원 관리 화면의 `employee-form-modal.tsx`와 동일한 패턴으로 `project` prop 전달 시 수정 모드(`PATCH`)로 동작, 미전달 시 기존과 동일하게 등록 모드(`POST`)로 동작. 프로젝트 코드(`PJT_CD`)는 수정 불가 처리(UNIQUE 제약, 사원 상세의 사번 처리와 동일 원칙). `projects/page.tsx`는 이 공용 컴포넌트를 import해 인라인 정의를 제거(등록 동작은 기존과 동일하게 유지), `projects/[id]/page.tsx`에 "수정" 버튼을 추가하고 상세 데이터를 재조회할 수 있도록 `reload`를 named 함수로 분리. 백엔드 변경 없음, pytest 107개 그대로 통과. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 임시 프로젝트 1건을 등록해 curl로 `PATCH` 호출 시 프로젝트명·고객사·상태가 정상 반영됨을 확인, 검증에 사용한 임시 프로젝트는 SQL로 삭제. `/projects`, `/projects/{pjt_id}` 페이지 200 렌더링 확인. §9-1 "프로젝트 상세 화면 수정 버튼/폼" 항목 `[x]` 처리(같은 화면의 "종료처리"·"인력투입" 버튼은 이번 범위에서 다루지 않아 미완료로 유지)
- **프로젝트 상세 화면 종료처리 버튼 구현 (§9-1 다음 미완료 항목)** — 목록 순서상 다음 미완료 항목인 "프로젝트 상세 화면 — 종료처리 버튼 없음"을 처리. 백엔드 `PATCH /api/v1/projects/{pjt_id}`(이미 구현, `projects.update` 권한)로 `PJT_STAT_CD`만 `CLOSED`로 변경하면 되므로 백엔드 변경 없이 프론트엔드 연동만 추가. 사원 상세 화면의 "퇴직처리" 버튼과 동일한 패턴 — 이미 사원 상세에서 사용 중인 공용 `ConfirmDialog`를 재사용해 "종료처리" 버튼 클릭 시 확인 다이얼로그(`destructive` 스타일)를 거쳐 `PATCH`를 호출, 이미 종료된 프로젝트(`PJT_STAT_CD==='CLOSED'`)는 버튼을 비활성화해 불필요한 재요청을 UI에서 방지, 처리 성공 시 상세 데이터 재조회(`reload`)로 상태 배지 즉시 반영. 백엔드 변경 없음, pytest 107개 그대로 통과. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 임시 프로젝트 1건을 등록해 curl로 `PATCH`(`PJT_STAT_CD: 'CLOSED'`) 호출 시 정상 전환됨을 확인, 검증에 사용한 임시 프로젝트는 SQL로 삭제. `/projects/{pjt_id}` 페이지 200 렌더링 확인. §9-1 "프로젝트 상세 화면 종료처리 버튼" 항목 `[x]` 처리(같은 화면의 "인력투입" 버튼은 이번 범위에서 다루지 않아 미완료로 유지)
- **프로젝트 상세 화면 인력투입 버튼 구현 (§9-1 다음 미완료 항목)** — 목록 순서상 다음 미완료 항목인 "프로젝트 상세 화면 — 인력투입 버튼 없음"을 처리. 백엔드 `POST /api/v1/assignments`는 이미 구현되어 있어 프론트엔드 연동만 추가. 그동안 투입 관리 화면(`assignments/page.tsx`)에 인라인 함수로만 존재하던 실 API 연동 등록 모달을, 이미 저장소에 있었으나 목데이터(`lib/mock-data.ts`) 기반이라 어디에서도 실제로 쓰이지 않던 `frontend/components/projects/assignment-form-modal.tsx`를 실 API 연동 공용 컴포넌트로 교체하며 그 자리에 추출 — 프로젝트 상세·수정·종료처리와 동일하게 이번에도 "인라인 실 구현 → 공용 컴포넌트 추출" 패턴을 재사용. `fixedPjtId`/`fixedPjtName` prop을 신규 추가해, 프로젝트 상세 화면에서 열 때는 프로젝트 Select 자체를 숨기고 현재 프로젝트로 고정 등록하며, 투입 관리 화면(프로젝트 선택 필요)에서는 기존과 동일하게 동작하도록 분기. `projects/[id]/page.tsx`의 `loadProjectDetail`이 이미 조회해 조인에만 쓰던 `employees` 원본 배열을 반환값에 노출(신규 API 호출 없이 재사용), 사원 옵션 표시에 필요한 `EMPL_NO` 필드도 함께 노출하도록 로컬 타입 확장. `assignments/page.tsx`는 이 공용 컴포넌트를 import해 인라인 정의를 제거(등록 동작은 기존과 동일하게 유지). 백엔드 변경 없음, pytest 107개 그대로 통과. **실 서버 컨테이너에서 실제 HTTP 호출로 검증**: 재빌드 후 임시 프로젝트·사원 각 1건을 등록해 curl로 `POST /api/v1/assignments` 호출 시 정상 등록(201)됨을 확인(기존 사원으로 시도 시 투입률 100% 초과로 409가 반환되는 기존 검증 로직도 함께 재확인), 검증에 사용한 임시 데이터는 SQL로 삭제. `/projects/{pjt_id}` 페이지 200 렌더링 확인. §9-1 "프로젝트 상세 화면 인력투입 버튼" 항목 `[x]` 처리 — 프로젝트 관리 섹션의 §9-1 항목 전부 완료

---

## 8. 다음 작업

> Rolling Backlog / Next Action Queue — 누적 완료 목록이 아니라 "지금부터 수행할 작업"만 유지한다.
> 완료된 작업은 이 섹션에 남기지 않고 §7 개발 완료 내역과 §11 MVP 구현 체크리스트에만 기록한다.

- [ ] 1. `HR_DATA_QUALITY_CHK` 배치 구현 (Phase 7, 매주 금요일 18:00 데이터 품질 점검 — 대시보드/리포트가 이미 사용 중인 데이터 품질 판정 로직(`get_data_quality`, `app/repositories/dashboard.py`)을 배치로 재사용해 주간 점검 이력을 `SYS_BATCH_HIS`에 기록, 필요 시 Teams 알림 포함)

> 참고: "`PJT_ASGN_END_ALERT` 배치 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다 — `backend/app/repositories/pjt_asgn_his.py`의 `list_ending_soon_assignments`, `backend/app/services/asgn_end_alert.py`의 `run_asgn_end_alert`, `backend/app/services/teams_notify.py`(신규, Teams Incoming Webhook 전송, 미설정 시 조용히 건너뜀)를 구현하고 `app/worker.py`에 매주 금 17:00(KST) cron으로 등록했다. `TEAMS_WEBHOOK_URL`이 `.env`에 미설정 상태라 실제 Teams 알림 전송 자체는 검증하지 못했다(§9 리스크 신규 기록) — 배치 로직·이력 기록은 실 서버에서 정상 동작 확인. Phase 7 진행률이 10%→20%로 상승했다.

> 참고: "`HR_AVAIL_SNAP_GEN` 배치 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다 — `backend/app/services/avail_snap_gen.py`(`run_avail_snap_gen`, `SYS_BATCH_HIS` 이력 기록)와 `backend/app/worker.py`(APScheduler `BlockingScheduler`, KST 매일 01:00 cron)를 신규 구현, `worker` 컨테이너 재빌드 후 스케줄러 정상 기동 및 배치 수동 실행으로 재직 사원 전체 스냅샷 생성·재실행 시 멱등성까지 확인했다. 이 항목 완료로 Phase 5의 마지막 잔여 항목("가동 가능일 자동 계산 로직 구현")도 함께 완료 처리되어 Phase 5가 100%가 되었다(Phase 7은 10%). 단, 대시보드(`dashboard.py`)·리포트(`reports.py`) API는 여전히 스냅샷을 조회하지 않고 실시간 재계산 방식을 그대로 사용 중이다(§9 기존 리스크 2건 유지 — 스냅샷 기반 조회로의 전환은 이번 범위 밖). 다음 순서는 §4 Phase 7 "주요 작업" 표에서 이어지는 "`PJT_ASGN_END_ALERT` 배치 구현"이다.

> 참고: "권한 필터링 후 LLM 컨텍스트 전달 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다 — `POST /api/v1/ai/chat`이 `resource_search` 응답 직전 요청자 `PERM_JSON`의 `availability.view` 권한을 확인하도록 수정(`app/api/deps.py`의 `has_permission` 신규 유틸), 없으면 조회를 실행하지 않고 안내 메시지만 반환. VIEWER로 차단 재현·검증 완료. Phase 6 진행률이 63%→75%로 상승했다. 부서 단위 등 행(row) 단위 권한 세부 범위 제한은 여전히 미구현 상태로 남아있다(§9 참조, 필요 시 별도 항목화 검토).

> 참고: "자연어 조건 파싱 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다 — 사용자가 "AI Chat 1차 구현 범위에서 SQL 조회·권한 필터링·환각 방지까지 한 번에 포함하지 말자는 것이었을 뿐 영구 제외는 아니다"라고 명확히 하며 착수를 승인, `backend/app/services/ai_parser.py`(신규)로 규칙 기반 파싱만 구현하고 SQL 조회는 이번 범위에서 수행하지 않았다. Phase 6 진행률이 38%→50%로 상승했다. 다음 순서는 사용자가 이미 순차 진행을 확정한 "파싱 결과 → SQL 조회 → 결과 요약 흐름 구현"이며, 착수 시에도 LLM이 임의 SQL을 생성하지 않도록 whitelist 기반 intent(`resource_search`)와 기존 repository/query builder만 사용해야 한다(사용자 지침).

> 참고: "직무 유형·기술·숙련도 복합 필터 검색 API 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다 — `GET /api/v1/availability`에 `skill_id`/`min_prfcy_levl` 파라미터를 추가해 Phase 5 진행률이 75%→88%로 상승했다. Phase 5의 유일한 잔여 항목("가동 가능일 자동 계산 로직 구현")은 Phase 7 배치 구현이 선행되어야 해(§9 리스크 참조) 큐에 포함하지 않았고, §3/§4 로드맵상 다음 순서인 Phase 6(AI 질의응답 연동, 38%)의 "주요 작업" 표에서 가장 앞선 미완료 항목으로 큐를 재구성했다. 단, Phase 6의 자연어 파싱·SQL 조회·권한 필터링·환각 방지 4개 항목은 지난 턴에 사용자가 "AI Chat 화면 구현과 분리해 별도 후속 작업으로 진행"하기로 명시적으로 확정한 사안이라, 착수 전 범위·우선순위를 사용자에게 재확인하는 것을 권장한다.

> 참고: "설정 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다. 사용자 관리·감사 로그 조회만 구현했고, 계정 수정/비활성화·감사 로그 Excel 내보내기는 후속 작업으로 분리했다(§9 리스크 참조).

> 참고: "리포트 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다. 주간/월간 탭만 구현했고, "월별 가동률 통계" 매트릭스 탭·리포트 발송·Excel 내보내기는 후속 작업으로 분리했다(§9 리스크 참조).

> 참고: "AI Chat 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다. 사용자 확정에 따라 1차 범위(LLM 단순 호출/응답)만 구현했고, 자연어 조건 파싱·SQL 조회 연동은 Phase 6 후속 작업으로 별도 분리했다(§4 Phase 6 표 참조).

> 참고: "리소스 추천 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다. 백엔드 API(`PJT_RSRC_REQ`/`PJT_RCMD_RSLT`)가 없어 이번 작업에서 함께 신규 구현했다.

> 참고: "가동 가능 인력 조회 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

> 참고: "투입 관리 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

> 참고: "프로젝트 목록/상세 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

> 참고: "직무 유형 관리 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

> 참고: "기술 관리 화면 구현"은 2026-07-04에 완료되어(§7, §11 참조) 이 큐에서 제외했다.

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
| `PJT_ASGN_END_ALERT` 배치의 Teams 알림 실제 전송 미검증 | 낮음 | 주의 | `.env`에 `TEAMS_WEBHOOK_URL`이 설정되어 있지 않아, `app/services/teams_notify.py`가 알림 전송을 건너뛰는 코드 경로만 실 서버에서 확인했고 실제 Teams 채널로의 발송 자체는 검증하지 못했다. 배치 로직(대상 조회, `SYS_BATCH_HIS` 기록)은 정상 동작 확인 완료 — 운영팀이 Teams 채널의 수신 커넥터(Incoming Webhook) URL을 발급받아 `.env`(직접 수정 금지 원칙에 따라 운영자가 직접 설정)의 `TEAMS_WEBHOOK_URL`에 설정하면, 다음 배치 실행 시 자동으로 실제 전송 경로를 타게 된다 — 별도 코드 변경 불필요 | 2026-07-04 |
| AI Chat `resource_search` 조회 결과에 권한 필터링 미적용 | 중간 | 해소 | `POST /api/v1/ai/chat`에서 `intent="resource_search"` 응답 직전 요청자 `PERM_JSON`의 `availability.view` 권한을 추가 확인하도록 수정(`app/api/deps.py`의 `has_permission` 신규 유틸 재사용) — 권한 없으면 조회 자체를 실행하지 않고 안내 메시지만 반환. VIEWER로 재현·검증 완료. 단, 부서 단위 등 행(row) 단위 세부 범위 제한(예: "본인 부서 인력만")은 기존 `require_permission`과 동일한 한계로 여전히 미구현 — 필요 시 별도 항목으로 재검토 | 2026-07-04 |
| `GET /api/v1/employees/export`가 `GET /{empl_id}` 라우트에 가로채여 항상 422 반환 | 높음 | 해소 | Excel Import/Export UI 프론트엔드 연동 작업 중 curl 검증으로 발견 — FastAPI는 라우트를 등록 순서대로 매칭하는데 `/{empl_id}`(UUID 경로)가 `/export`보다 먼저 등록되어 "export" 문자열이 UUID 파싱에 실패해 422를 반환하고 있었음(한 번도 정상 동작한 적 없던 기존 버그). `backend/app/api/v1/employees.py`에서 `/export`·`/import` 라우트를 `/{empl_id}` 라우트보다 앞으로 이동해 수정, `backend/tests/test_employees_excel.py` 회귀 방지 테스트 추가 | 2026-07-04 |
| 직원 기술 스택 표준화 기준 미정 | 높음 | 해소 | 사용자 확정 기준으로 `HR_SKILL_MST` 표준 Seed 110건(LANGUAGE/BACKEND/FRONTEND/MOBILE/DB/DATA/INFRA/SECURITY/ARCHITECTURE/QA/CONSULTING/PMO/BUSINESS(금융) 13개 그룹) 작성 및 Alembic 마이그레이션(`55106956dedf`)으로 실 DB 반영 완료 — `backend/app/db/seed/hr_skill_mst_seed.py` 참조. 기존 MVP 초안(6개 그룹, DB 미반영)을 대체. 기술명은 Excel Import "주요기술" 컬럼과 매핑되는 표준 영문/일반 명칭으로 작성 | 2026-07-04 |
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
| `PJT_RCMD_RSLT` 추천 점수 가중치 표기 불일치 | 낮음 | 해소 | 설계 문서 §5 인용 구간과 로드맵 §4 Phase 5·§11 명시 가중치 수치가 다르게 표기되어 있었음 — 추천 점수 산정 로직 구현 시(2026-07-04) 로드맵 수치(직무 15%+기술 35%+숙련도 25%+가동일 15%+유사경험 7%+역할적합도 3%)로 확정해 `backend/app/repositories/pjt_rcmd_rslt.py`에 반영 완료 | 2026-07-04 |
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
| 사원 상세 화면의 정보수정·기술추가·퇴직처리 UI 미구현 | 중간 | 해소 | 사원 상세 화면(SCR-004)을 실 API로 연동하면서 조회(기본정보/보유기술/투입이력) 기능만 구현하고 편집 기능은 제외했던 리스크 — 정보수정(2026-07-04), 기술추가(2026-07-04)에 이어 퇴직처리 버튼까지 구현 완료(2026-07-04, `ConfirmDialog` 재사용 + `DELETE /api/v1/employees/{empl_id}` 연동)되어 3개 항목 전부 해소. §9-1 해당 항목들 `[x]` 처리 완료 | 2026-07-04 |
| 사원 상세 화면 "변경 이력" 탭 미구현 — 감사 로그 조회 API 부재 | 낮음 | 해소 | 설정 화면(SCR-016) 구현 시 확보된 `GET /api/v1/audit-logs`에 `tgt_id` 단건 필터를 신규 추가하고 사원 상세 화면에 "변경 이력" 탭 UI를 연동 완료(2026-07-05) — 리스크 해소. 단, 이 탭은 `settings_audit_logs.view`(Admin 전용) 권한이 있어야 조회 가능해(설계서 SCR-016 원칙 유지) 일반 사용자는 탭 진입 시 "조회 권한이 없습니다" 안내만 표시됨(신규 제약 아님, 기존 권한 정책 그대로 적용) | 2026-07-05 |
| `HR_DEPT_MST`(부서 마스터) Seed 데이터 없음 | 중간 | 주의 | 사원 상세 화면 검증 중 실 DB에 `HR_DEPT_MST`가 0건(부서 코드 미시딩)임을 확인 — `HR_JIKGUP_MST`(직급, 10건)와 `HR_SKILL_MST`(기술, 1건, 비활성)는 일부 존재하나 부서는 전혀 없어 사원 등록·조회 화면에서 부서 필터/표시가 항상 빈 목록으로 나타남. 운영팀 확정 부서 목록 확보 후 Seed 스크립트(`backend/app/db/seed/`) 추가 필요 | 2026-07-03 |
| `hrm-worker` 컨테이너가 재시작 루프 상태 | 중간 | 주의 | 사원 상세 화면 작업 중 `docker compose ps` 확인 과정에서 `hrm-worker` 컨테이너가 `Restarting (0)` 상태로 반복 재기동 중임을 발견 — 이번 작업과 무관한 기존 이슈로 원인 미조사(범위 밖). 백그라운드 배치/추천 작업이 필요한 Phase(§4 이후)에서 워커가 실제로 사용되기 전에 원인 확인 및 조치 필요 | 2026-07-03 |
| `HR_SKILL_MST.SKILL_NM`에 유니크 제약 없음 — 중복 등록 시 오류 미발생 | 낮음 | 해소 | 기술 관리 화면(SCR-005) 실 API 연동 검증 중 동일 `SKILL_NM`으로 두 번 `POST /api/v1/skills`를 호출해도 둘 다 201로 성공함을 확인해 리스크로 기록했던 건 — `HR_SKILL_MST` 표준 Seed 작성 작업(2026-07-04)과 함께 Alembic 마이그레이션(`55106956dedf`)에서 `(SKILL_GRP_CD, SKILL_NM)` 복합 UNIQUE 제약(`uq_hr_skill_mst_grp_nm`)을 추가해 해소 — 동일 조합 재등록 시 API가 409를 정상 반환함을 재검증 완료(`backend/tests/test_skills.py` 회귀 테스트 추가). 기존 데이터에 중복이 없음을 확인한 뒤 제약을 적용해 마이그레이션 실패 없이 반영됨 | 2026-07-04 |
| SSH 터널 등 접속 방식에 따라 프론트엔드가 백엔드에 연결 못하는 구조적 한계 | 높음 | 해소 | 사용자가 "SSH 터널로 `localhost:3030` 접속 시 로그인 화면에서 '서버에 연결할 수 없습니다' 오류"를 보고. 원인은 CORS가 아니라, 빌드 시점에 고정되는 `NEXT_PUBLIC_API_BASE_URL`이 서버의 LAN IP(`http://192.168.0.87:8000`)로 절대경로 고정되어 있어, SSH 로컬 포트 포워딩(`localhost:포트`만 가로챔)을 거치지 않고 클라이언트 PC가 그 LAN IP로 직접 연결을 시도하다 실패하는 구조였음(같은 LAN이 아니면 연결 자체 불가) — 요청이 서버에 도달하기 전에 실패해 `hrm-api` 로그에도 기록이 남지 않음과 일치. `frontend/next.config.mjs`에 `rewrites()`를 추가해 `/api/v1/*` 요청을 Next.js 서버가 Docker 내부망의 `api:8000` 컨테이너로 대신 전달하도록 프록시 구성 — 프론트엔드 코드는 `NEXT_PUBLIC_API_BASE_URL`이 빈 값이면 상대 경로로 호출하도록 이미 되어 있어 코드 변경 없이 프록시를 자동으로 타게 됨. 사용자가 `.env`의 `NEXT_PUBLIC_API_BASE_URL`을 빈 값으로 변경(AI는 `.env` 직접 수정 금지, 안내만 제공) 후 재빌드해 LAN IP 직접 접속과 SSH 터널(3030 포트 하나만 필요) 두 접속 방식을 하나의 빌드로 동시 지원하도록 구조적으로 해소 | 2026-07-04 |
| 리소스 추천 점수 산정 공식이 설계서에 세부 정의되어 있지 않음 — MVP 해석 적용 | 중간 | 주의 | 설계서(SCR-011)는 6개 항목의 가중치 비율(직무 15%+기술 35%+숙련도 25%+가동일 15%+유사경험 7%+역할적합도 3%)만 명시하고 항목별 세부 산정 공식은 없음 — `backend/app/repositories/pjt_rcmd_rslt.py`에 MVP 해석으로 구현: 직무는 정확히 일치해야 만점(부분 유사 미고려), 기술은 요청 기술 대비 보유 비율, 숙련도는 매칭된 기술의 평균 숙련도(1~5) 비율, 가동일은 희망일 이내 가동 가능 여부의 이진 판정(부분 점수 없음), 유사경험은 요청 역할명과 일치하는 과거(DONE) 투입 건수(최대 3건=만점), 역할 적합도는 유사경험 존재 여부의 이진 판정. `REQ_SKILL_JSON`도 설계서에 내부 스키마가 없어 `{"SKILL_IDS": [...], "MIN_PRFCY_LEVL": n}` 구조로 자체 정의. 운영팀 확인 후 필요 시 산정 공식 조정 필요 | 2026-07-04 |
| 리소스 추천 화면 UI 축소 — 다중 기술 선택·"이 후보로 투입 요청" 버튼 미구현 | 낮음 | 주의 | 설계서(SCR-011)는 기술을 여러 개 칩(chip)으로 추가/삭제할 수 있어야 하나, 이번 구현은 기존 프로토타입과 동일하게 단일 기술 선택만 지원(`REQ_SKILL_JSON.SKILL_IDS`는 배열이라 백엔드는 다중 기술을 이미 지원하나, 프론트엔드 입력 UI만 단일 선택으로 제한). 추천 결과에서 "이 후보로 투입 요청"(권한 A H P) 버튼으로 실제 투입(`PJT_ASGN_HIS`) 등록까지 이어지는 흐름도 이번 범위에서 제외 — 결과 조회까지만 구현. 두 가지 모두 후속 작업으로 분리 | 2026-07-04 |
| AI Chat(Phase 6) LLM 연동 사전 점검 및 1차 구현 범위 확정 (사용자 확정) | 중간 | 해소 | 사용자가 `.env`에 `LLM_PROVIDER`/`DEEPSEEK_API_KEY`/`DEEPSEEK_BASE_URL`/`DEEPSEEK_MODEL_ID`를 이미 설정해뒀다고 확인 — AI가 실행 환경에서 DeepSeek API로 실제 인증 요청을 보내 정상 응답(200, 모델 답변 수신)을 받아 네트워크·인증 모두 문제없음을 검증 완료(키 값은 화면에 노출하지 않고 서버 프로세스 환경변수로만 사용). **1차 구현 범위를 사용자가 명시적으로 확정**: 이번 §8 "AI Chat 화면 구현" 작업은 `POST /api/v1/ai/chat`(LLM 단순 호출/응답)과 `/ai-chat` 자유 대화형 UI만 구현하고, §4 Phase 6 "주요 작업" 표의 "자연어 조건 파싱"·"파싱 결과→SQL 조회→요약 흐름"·"권한 필터링 후 LLM 컨텍스트 전달"·"환각 방지 프롬프트"·"테스트 질의 10개 검증"은 별도 후속 작업으로 분리(표에 반영 완료). `backend/app/core/config.py`(`Settings`)에 이 환경변수들을 읽는 필드가 아직 없어 착수 시 함께 추가 필요(소스코드 변경, `.env` 자체는 수정하지 않음), `.env.example`도 실제 `.env` 구성과 맞지 않아 함께 갱신 필요 | 2026-07-04 |
| 리포트 화면 "월별 가동률 통계" 매트릭스·리포트 발송·Excel 내보내기 미구현 | 중간 | 주의 | 설계서(SCR-013)는 3개 탭(주간/월간/월별 가동률 통계)과 리포트 수동 발송(Teams Webhook)·통계 매트릭스 Excel 내보내기를 요구하나, 이번 구현은 주간/월간 리포트(공용 요약+부서별 가동률+기술 분포)만 다루고 세 기능은 제외 — "월별 가동률 통계"는 인원별 다중 프로젝트 행+12개월 컬럼+소계+3단계 조직 평균+100% 초과 셀 강조까지 필요해 구조가 복잡하고, 발송/Excel 내보내기는 `TEAMS_WEBHOOK_URL` 연동·엑셀 생성 로직이 각각 별도로 필요해 "최소 단위" 원칙에 따라 후속 작업으로 분리. 화면에는 "월별 가동률 통계는 준비 중입니다" 안내만 표시 | 2026-07-04 |
| 리포트 API가 특정 시점의 과거 스냅샷을 보관하지 않음 | 낮음 | 주의 | `GET /reports/{weekly,monthly}`는 지정한 주차/월 시점 기준으로 **현재 데이터를 즉시 재계산**한 결과를 반환한다(대시보드 API와 동일한 `HR_AVAIL_SNAP` 배치 미구현 제약, §9 기존 리스크 "대시보드가 실시간 계산 사용" 참조) — 예를 들어 지난달 리포트를 조회해도 그 시점 당시의 실제 데이터가 아니라 현재 DB 상태를 기준으로 계산된 값이 나온다. `HR_AVAIL_SNAP_GEN` 배치(Phase 7) 도입 후 과거 스냅샷 기반 조회로 전환 필요 | 2026-07-04 |
| 화면 검색 필터 옵션이 마스터 데이터와 다르게 하드코딩되어 있던 문제 | 중간 | 해소 | 사용자가 "각 화면의 검색 필터 항목이 DB에서 조회되는지, 하드코딩되어 있는지" 질의해 전체 화면을 감사한 결과, `HR_SKILL_MST` 표준 Seed 재작성(§7 2026-07-04) 이후 **기술 관리(`/skills`) 화면의 "기술 그룹" 필터가 `frontend/lib/options.ts`에 하드코딩된 옛 7개 그룹**(BACKEND/FRONTEND/DB/CLOUD/DEVOPS/DESIGN/BUSINESS)을 그대로 쓰고 있어, 실제 새 Seed의 13개 그룹(LANGUAGE/BACKEND/FRONTEND/MOBILE/DB/DATA/INFRA/SECURITY/ARCHITECTURE/QA/CONSULTING/PMO/BUSINESS) 중 다수가 필터로 선택 불가능한 상태임을 발견 — 즉시 수정: `skillGroupOptions`(하드코딩) 제거, 화면에서 실제로 불러온 기술 목록의 `SKILL_GRP_CD` distinct 값으로 필터·등록 모달 그룹 목록을 동적 생성하도록 변경. 직무 유형(`/job-types`) 화면의 "그룹" 필터도 같은 문제로 함께 점검 — 등록/수정 모달은 설계서(SCR-006)가 명시한 고정 3종(TECHNICAL/MANAGEMENT/ANALYSIS)을 의도적으로 유지하되(신규 등록 시 그룹명 난립 방지), 필터 드롭다운만 실제 데이터 기반으로 동적 생성하도록 분리 수정. 나머지 화면(가동 가능 인력·리소스 추천의 조직/직무유형/기술 필터)은 이미 실 API 기반이라 문제 없음을 확인, 상태/유형 계열 필터(프로젝트 상태·투입 유형 등)는 DB CHECK 제약과 동일한 고정 열거값이라 하드코딩이 의도된 정상 설계임도 함께 확인 | 2026-07-04 |

### 9-1. 완료 표시된 화면의 미구현 세부 기능 — 후속 보완 체크리스트

> "완료"로 표시된 화면·API라도 조회 전용으로만 구현되었거나, 설계서 대비 일부 기능이 빠진 경우를 모아 놓친 것이 없도록 정리한다. 각 항목의 상세 배경은 위 리스크 표 또는 §7 개발 완료 내역을 참고. 이 체크리스트 자체는 §8 다음 작업 큐에 자동 편입되지 않으며, 실제 착수 시 §8에 신규 항목으로 추가한다.

**사원 관리 (`/employees`, `/employees/[id]`)**
- [x] 사원 목록 화면 — `GET /api/v1/employees` 실 API 연동 완료 (2026-07-04, 신규 `GET /api/v1/employee-roles` 포함)
- [x] 사원 목록 "사원 등록" 모달 — `POST /api/v1/employees` 실 API 연동 완료 (2026-07-04). 조직/직급 Select를 부모(`employees/page.tsx`)가 이미 조회해둔 실 마스터 데이터(`DEPT_ID`/`JIKGUP_ID`)로 교체, 등록 성공 시 목록 새로고침(`onSaved`). 수정(edit) 모드는 이번 범위에서 다루지 않음 — 사원 상세 화면 "정보수정" 버튼/폼 자체가 아직 없어(§9-1 별도 항목) 진입점이 없음
- [x] 사원 상세 화면 — 정보수정 버튼/폼 구현 완료 (2026-07-04). `components/employees/employee-form-modal.tsx`에 수정 모드(`employee` prop 전달 시 `PATCH /api/v1/employees/{empl_id}`) 추가, 사원 목록 "사원 등록" 모달과 동일 컴포넌트 재사용(사번은 수정 불가 처리)
- [x] 사원 상세 화면 — 기술추가 버튼/폼 구현 완료 (2026-07-04). `components/employees/employee-skill-form-modal.tsx`(신규) — `POST /api/v1/employee-skills` 연동, 이미 보유한 기술은 선택지에서 제외해 중복 등록(409) 사전 방지. 기술 항목 수정(`PATCH`)은 이번 범위에서 다루지 않음(별도 후속)
- [x] 사원 상세 화면 — 퇴직처리 버튼 구현 완료 (2026-07-04). 기존 `frontend/components/common/confirm-dialog.tsx`(재사용 가능한 확인 다이얼로그, 그동안 다른 화면에서 미사용 상태였음)를 처음으로 연결해 "퇴직처리" 버튼 클릭 시 확인 후 `DELETE /api/v1/employees/{empl_id}` 호출(신규 `apiDelete` 헬퍼를 `lib/api.ts`에 추가). 이미 퇴직 처리된 사원은 버튼 비활성화(`EMPL_STAT_CD==='RETIRED'`), 처리 후 상세 데이터 재조회
- [x] 사원 상세 화면 "변경 이력" 탭 구현 완료 (2026-07-05). `GET /api/v1/audit-logs`에 `tgt_id` 필터 파라미터 신규 추가, 사원 상세 화면에 "변경 이력" 탭 UI 연동(`tgt_tbl_nm=HR_EMPL_MST&tgt_id={empl_id}`로 조회). `settings_audit_logs.view`(Admin 전용) 권한이 없는 사용자는 403이 반환되므로, 탭 클릭 시점에만 지연 조회하고 403은 화면 전체 에러가 아니라 탭 내부에 "조회 권한이 없습니다" 안내로 표시(다른 오류와 구분). 감사 로그 상세(BFR/AFT_VAL_JSON) 조회는 설정 화면의 감사 로그 탭에서 이미 제공하므로 이번 범위에서는 시각/작업/수행자만 표시하는 목록으로 최소 구현

**프로젝트 (`/projects`, `/projects/[id]`)**
- [x] 프로젝트 상세 화면 — 수정 버튼/폼 구현 완료 (2026-07-05). 그동안 프로젝트 목록 화면(`projects/page.tsx`)에 인라인으로만 있던 등록 전용 모달을 `components/projects/project-form-modal.tsx`(신규, 그동안 목데이터 기반으로 미사용 상태이던 동일 이름의 파일을 실 API 연동 공용 컴포넌트로 교체)로 추출 — `project` prop 전달 시 수정 모드(`PATCH /api/v1/projects/{pjt_id}`)로 동작, 프로젝트 코드는 수정 불가(사원 상세의 사번 처리와 동일 원칙, UNIQUE 제약)
- [x] 프로젝트 상세 화면 — 종료처리 버튼 구현 완료 (2026-07-05). 사원 상세 화면의 "퇴직처리"와 동일한 패턴으로 공용 `ConfirmDialog`를 재사용해 "종료처리" 버튼 클릭 시 확인 후 `PATCH /api/v1/projects/{pjt_id}`(`PJT_STAT_CD: 'CLOSED'`)만 호출. 이미 종료된 프로젝트는 버튼 비활성화(`PJT_STAT_CD==='CLOSED'`)
- [x] 프로젝트 상세 화면 — 인력투입 버튼 구현 완료 (2026-07-05). 그동안 투입 관리 화면(`assignments/page.tsx`)에 인라인 함수로만 있던 실 API 연동 등록 모달을, 이미 저장소에 있었으나 목데이터 기반이라 미사용 상태이던 `components/projects/assignment-form-modal.tsx`를 실 API 연동 공용 컴포넌트로 교체하며 그 자리에 추출 — `fixedPjtId`/`fixedPjtName` prop 전달 시(프로젝트 상세 화면) 프로젝트 선택 없이 고정값으로 등록, 미전달 시(투입 관리 화면) 기존과 동일하게 프로젝트를 선택해 등록

**리소스 추천 (`/recommendations`)**
- [ ] 필요 기술 선택이 1개만 가능(다중 칩 선택 UI 미구현 — 백엔드 `REQ_SKILL_JSON.SKILL_IDS`는 배열 지원)
- [ ] "이 후보로 투입 요청" 버튼 없음 — 추천 결과 → 실제 투입(`PJT_ASGN_HIS`) 등록 연결 흐름 전체 미구현

**가동 가능 인력 (`/availability`)**
- [ ] 기술·숙련도 필터 미구현 (`GET /api/v1/availability`는 직무 유형·부서 필터만 지원)

**AI Chat (`/ai-chat`)**
- [x] 자연어 조건 파싱 — `backend/app/services/ai_parser.py` 신규 구현 완료(2026-07-04)
- [x] 파싱 결과 → SQL 조회 → 결과 요약 흐름 — `backend/app/services/ai_resource_search.py`(신규) `search_resources`가 whitelist 기반으로 기존 `list_availability` repository를 호출, `POST /api/v1/ai/chat`이 조건 인식 시 LLM 없이 결정적 요약을 응답(2026-07-04). 기술 조건은 1개까지만 조회에 반영(단일 `skill_id` 제약, 나머지는 `skipped_skills`로 안내) — 다중 기술 AND 조회는 후속 확장 대상
- [x] 권한 필터링 후 LLM 컨텍스트 전달 — `availability.view` 권한 확인 후에만 조회 실행하도록 수정 완료(2026-07-04). 화면(screen) 단위 권한만 확인하며, 부서 단위 등 행(row) 단위 세부 범위 제한은 미구현
- [x] 환각 방지 시스템 프롬프트 적용 완료(2026-07-04) — `call_llm`(intent="unknown" 자유 응답 경로)이 매 호출 시 시스템 메시지로 지침 전달. resource_search 경로는 LLM 미경유라 애초에 해당 없음

**리포트 (`/reports`)**
- [x] "월별 가동률 통계" 매트릭스 탭 — `GET /api/v1/reports/utilization-matrix`(신규) + `components/reports/utilization-matrix.tsx` 실 데이터 연동 완료(2026-07-04). 인원별 다중 프로젝트 행/월별 컬럼/소계/3단계 조직 평균/100% 초과 강조 전부 구현. 리포트 수동 발송·가동률 통계 Excel 내보내기는 여전히 미구현(아래 항목)
- [ ] 리포트 수동 발송 미구현 (`TEAMS_WEBHOOK_URL` 연동 필요)
- [ ] 가동률 통계 Excel 내보내기 미구현

**설정 (`/settings`)**
- [ ] 계정 수정 기능 없음 (`PATCH /api/v1/users/{user_id}` 미구현 — 역할 변경 등)
- [ ] 계정 비활성화 기능 없음 (`DELETE /api/v1/users/{user_id}` 미구현 — `USE_YN=FALSE` 전환)
- [ ] 감사 로그 Excel 내보내기 미구현 (`GET /api/v1/audit-logs/export`)
- [x] 감사 로그 `tgt_id`(대상 ID) 단건 필터 구현 완료 (2026-07-05) — 사원 상세 화면 "변경 이력" 탭 구현과 함께 `GET /api/v1/audit-logs`에 `tgt_id` 파라미터 추가(위 "사원 관리" 섹션 항목 참조, 동일 작업)
- [ ] "일반 설정" 탭(조직 정보/가동률 정책) 여전히 목데이터 — 저장 버튼이 실제로 아무것도 하지 않음(이번 작업 범위는 사용자 관리·감사 로그 2개 탭만 포함)

**인증/감사 로그 (전역)**
- [ ] 로그아웃 시 서버 측 즉시 토큰 무효화 미구현 (stateless JWT — Redis 블랙리스트 등 후속 검토)

**기타 백엔드**
- [ ] 부서(`HR_DEPT_MST`)/직급(`HR_JIKGUP_MST`) 등록·수정 API 없음(조회만 가능) — 전용 관리 화면 자체가 백로그에 없어 필요 시 신규 항목화 검토
- [x] `HR_AVAIL_SNAP_GEN` 배치 구현 완료 (2026-07-04, `app/services/avail_snap_gen.py`+`app/worker.py`) — 단, 대시보드/리포트 API는 아직 스냅샷을 조회하지 않고 계속 실시간 재계산 방식을 사용 중(§9 리스크 "대시보드 API가 HR_AVAIL_SNAP 대신 실시간 계산 사용" 참조) — 스냅샷 기반 조회로의 전환은 별도 후속 작업

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
- [x] `HR_SKILL_MST` Seed 입력 — 사용자 확정 기준 표준 Seed 110건(13개 그룹: LANGUAGE/BACKEND/FRONTEND/MOBILE/DB/DATA/INFRA/SECURITY/ARCHITECTURE/QA/CONSULTING/PMO/BUSINESS) 작성 및 Alembic 마이그레이션(`55106956dedf`)으로 실 DB 반영 완료, `(SKILL_GRP_CD,SKILL_NM)` 복합 UNIQUE 제약 추가로 중복 방지, `alembic upgrade/downgrade` 양방향 실 서버 검증 완료 (2026-07-04)
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
- [x] 리소스 검색/추천 API (`PJT_RSRC_REQ`, `PJT_RCMD_RSLT`) — `POST /api/v1/resource-requests`, `POST /api/v1/recommendations/score`, `GET /api/v1/recommendations/{req_id}` 구현, 실 서버 검증 완료 (2026-07-04)
- [x] 직무 유형·기술·숙련도 복합 필터 검색 API — `GET /api/v1/availability`에 `skill_id`/`min_prfcy_levl` 쿼리 파라미터 신규 추가(기존 직무 유형·부서 필터와 복합 적용), 실 서버 검증 완료 (2026-07-04)
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
- [x] 기술 관리 화면 구현 (`/skills`, `HR_SKILL_MST`) — 목데이터를 백엔드 실 API(조회/등록/수정)로 전량 교체, 사용여부 토글은 기존 `PATCH` 재사용, 실 서버 검증 완료 (2026-07-04)
- [x] 직무 유형 관리 화면 구현 (`/job-types`, `HR_JIKMU_MST`) — 목데이터를 백엔드 실 API로 전량 교체, 등록/수정 API가 없어 `POST`/`PATCH /api/v1/job-types` 신규 추가, 실 서버 검증 완료 (2026-07-04)
- [x] 프로젝트 목록/상세 화면 구현 (`/projects`, `/projects/[id]`) — 목데이터를 백엔드 실 API로 전량 교체, `GET /api/v1/projects/{pjt_id}` 신규 추가, 실 서버 검증 완료 (2026-07-04). 수정/종료처리/인력투입은 조회 전용으로 남겨 후속 과제로 분리
- [x] 투입 관리 화면 구현 (`/assignments`, `PJT_ASGN_HIS`) — 목데이터를 백엔드 실 API로 전량 교체, 등록 모달 신규 추가(기존 등록/100% 초과 검증 API 재사용), 공수 초과 배정 감지 로직 실 데이터 기준으로 교체, 실 서버 검증 완료 (2026-07-04)
- [x] 가동 가능 인력 조회 화면 구현 (`/availability` — 직무 유형 필터 포함) — 목데이터를 백엔드 실 API로 전량 교체, `GET /api/v1/availability`(일괄 조회) 신규 추가, 사원/부서/직무/기술 마스터 조인, 실 서버 검증 완료 (2026-07-04)
- [x] 리소스 추천 화면 구현 (`/recommendations`, `PJT_RCMD_RSLT`) — 목데이터를 백엔드 실 API로 전량 교체, `PJT_RSRC_REQ`/`PJT_RCMD_RSLT` API 신규 추가, 실 서버 검증 완료 (2026-07-04)
- [x] AI Chat 화면 구현 (`/ai-chat`) — 1차 범위(사용자 확정): LLM 단순 호출/응답 + 자유 대화형 UI만 구현, 실 서버에서 DeepSeek API 실제 호출로 검증 완료 (2026-07-04). 자연어 조건 파싱·DB 조회 연동은 후속 작업으로 분리
- [x] 리포트 화면 구현 (`/reports`) — 주간/월간/월별 가동률 통계 매트릭스 3개 탭 전부 실 API 연동 완료(매트릭스는 2026-07-04 사용자 요청으로 추가 구현). `GET /api/v1/reports/{weekly,monthly,utilization-matrix}` 신규 추가, 실 서버 검증 완료. 리포트 발송·가동률 통계 Excel 내보내기는 후속 과제로 분리
- [x] 설정 화면 구현 (`/settings/users`, `/settings/audit-logs`) — 사용자 관리·감사 로그 조회를 백엔드 실 API로 전량 교체, `GET/POST /api/v1/users`, `GET /api/v1/users/roles`, `GET /api/v1/audit-logs` 신규 추가, 실 서버 검증 완료 (2026-07-04). 계정 수정/비활성화(`PATCH`/`DELETE /users`)·감사 로그 Excel 내보내기는 후속 과제로 분리
- [x] Excel Import/Export UI 구현 — 사원 목록 화면에 "Excel 가져오기/내보내기" 버튼 신규 추가, 기존 백엔드 API 연동, 실 서버 검증 완료 (2026-07-04). 검증 중 `GET /export`가 `/{empl_id}` 라우트에 가로채여 항상 422를 반환하던 기존 라우팅 버그를 발견해 함께 수정, 회귀 방지 테스트 추가. 사원 목록 화면 자체는 여전히 목데이터 기반 — 아래 프론트엔드 체크리스트 참조
- [x] 사원 목록 화면(`/employees`) 실 API 연동 (사용자 요청) — `GET /api/v1/employees`+`departments`/`positions`/`job-types`/`employee-roles`(신규)/`availability` 병렬 조회 후 클라이언트 조인, 실 서버 검증 완료 (2026-07-04). 프로젝트 목록 화면(`/projects`)은 이미 실 API 연동 상태임을 확인(§7 2026-07-04 항목 참조)

---

### 리소스 검색 및 추천 `→ Phase 5`

- [x] 가동 가능일 자동 계산 로직 구현 (`HR_AVAIL_SNAP` 기반, MVP 산정 기준 확정 — 기준일 `SNAP_DT` 기준 `ACTIVE`+`RUNNING/COMMITTED` 투입만 집계, `PROPOSED` 제외, 0%=`AVAILABLE`/1~99%=`PARTIAL`/≥100%=`FULL`(`MAX(ASGN_END_DT)+1`); 상세는 `backend/docs/AVAILABILITY_CALC_SPEC.md` 참조) — 즉시 계산 API(2026-07-03)에 이어 매일 01:00 배치 `HR_AVAIL_SNAP_GEN`(`app/services/avail_snap_gen.py`, `app/worker.py`)도 구현 완료 (2026-07-04). 단, 실 운영 환경에서의 실제 야간 배치 정상 동작(§10 "정식 운영 전환 기준" 5번)은 파일럿 운영 단계에서 별도 확인 필요
- [x] 즉시 투입 가능 인력 조회 API 구현 (`AVAIL_STAT_CD='AVAILABLE'`) — `GET /api/v1/availability`, 직무 유형·부서 필터 포함, 실 서버 검증 완료 (2026-07-04)
- [x] 직무 유형·기술·숙련도 복합 필터 검색 API 구현 — `GET /api/v1/availability`에 `skill_id`/`min_prfcy_levl` 파라미터 추가, 실 서버 검증 완료 (2026-07-04)
- [x] 추천 점수 산정 로직 구현 (2026-07-04)
  - 직무 유형 일치 15% + 기술 매칭 35% + 숙련도 25% + 가동일 15% + 유사 경험 7% + 역할 적합도 3%
  - 설계서에 항목별 세부 산정 공식이 없어 MVP 해석 적용(§9 리스크 참조) — `backend/app/repositories/pjt_rcmd_rslt.py`
- [x] `PJT_RSRC_REQ` 인력 요청 등록 API 구현 — `POST /api/v1/resource-requests`, 실 서버 검증 완료 (2026-07-04)
- [x] `PJT_RCMD_RSLT` 추천 결과 저장 및 조회 API 구현 — `POST /api/v1/recommendations/score`, `GET /api/v1/recommendations/{req_id}`, 실 서버 검증 완료 (2026-07-04)

---

### AI 질의응답 `→ Phase 6`

- [x] LLM 호출 레이어 추상화 (OpenAI/Anthropic/사내 LLM 전환 가능 구조) — `backend/app/services/ai_chat.py`의 `call_llm`, `LLM_PROVIDER` 설정값 기준 분기(현재 DeepSeek만 지원), 실 서버에서 DeepSeek API 실제 인증 호출 검증 완료 (2026-07-04)
- [x] 자연어 조건 파싱 구현 (`JIKMU_CD`, `SKILL_NM`, 가동일 키워드 인식 포함) — `backend/app/services/ai_parser.py`(신규) 규칙 기반 파싱, `ParsedResourceQuery` 표준 스키마 반환, 직무 유형·기술명·부서명·가동일/기간·숙련도 인식 + 미해석 조건(`unresolved_terms`) 기록, `backend/tests/test_ai_parser.py` 12개 케이스 검증 완료 (2026-07-04)
- [x] 파싱 결과 → SQL 조회 → 결과 요약 흐름 구현 — `backend/app/services/ai_resource_search.py`(신규) `search_resources`, whitelist(`intent="resource_search"`) 기반으로 기존 `list_availability` repository만 호출(free-form SQL 없음), `backend/tests/test_ai_resource_search.py` 4개 케이스 검증 완료 (2026-07-04)
- [x] 권한 필터링 후 LLM 컨텍스트 전달 구현 — `POST /api/v1/ai/chat`이 `resource_search` 응답 전 `availability.view` 권한을 확인, `backend/tests/test_ai_chat.py`에 VIEWER 차단 케이스 추가 검증 완료 (2026-07-04). 행(row) 단위(부서 범위 등) 세부 제한은 미구현으로 남음
- [x] 환각 방지 시스템 프롬프트 적용 — `call_llm`이 매 호출 시 환각 방지 시스템 메시지를 함께 전달, `backend/tests/test_ai_chat_service.py` 신규 검증 완료 (2026-07-04). `resource_search`(LLM 미경유) 경로는 대상 아님
- [x] `POST /api/v1/ai/chat` 엔드포인트 구현 — LLM 단순 호출/응답 + resource_search intent 시 whitelist 조회 기반 결정적 요약 응답, 권한 `ai_chat.view`(전 역할 허용), 실 서버 검증 완료 (2026-07-04)
- [x] 테스트 질의 10개 이상 검증 (직무 유형 포함) — `backend/tests/test_ai_chat_e2e.py`(신규) `POST /api/v1/ai/chat` 전체 경로 기준 10개 질의 검증 완료 (2026-07-04). Phase 6 전체 8개 항목 완료 — 100%

---

### 운영 자동화 및 배포 `→ Phase 7`

- [x] `HR_AVAIL_SNAP_GEN` 배치 구현 (매일 01:00 — 가동가능 스냅샷 생성) — `app/services/avail_snap_gen.py`+`app/worker.py`(APScheduler), 실 서버 컨테이너에서 스케줄러 기동·수동 실행·멱등성 확인 완료 (2026-07-04)
- [x] `PJT_ASGN_END_ALERT` 배치 구현 (매주 금요일 17:00 — 30일 이내 종료 예정 알림) — `app/services/asgn_end_alert.py`+`app/services/teams_notify.py`+`app/worker.py`, 실 서버 컨테이너에서 스케줄러 기동·배치 수동 실행·`SYS_BATCH_HIS` 기록 확인 완료 (2026-07-04). `TEAMS_WEBHOOK_URL` 미설정으로 실제 알림 전송 자체는 미검증(§9 참조)
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
| 2026-07-01 | v0.0.1 | ROADMAP 최초 작성 (Phase 0~8 구성, 기능·기술 요소 상태표, 리스크 초안) | — |
| 2026-07-01 | v0.0.2 | 설계 문서(v0.4) § 14.2 MVP 완료 체크리스트를 §11로 이관 — 인프라/DB/백엔드/프론트엔드/검색추천/AI/운영자동화/파일럿 8개 카테고리, 각 Phase 연결, 테이블 수준 세부 항목 추가 | — |
| 2026-07-02 | v0.0.3 | Phase 1 착수 — 디렉토리 구조, `docker-compose.yml`, `.env.example`, `.gitignore`, `README.md`, `backend`/`frontend` Dockerfile, FastAPI `/health` 스켈레톤, `backup_db.sh` 작성 완료. Phase 1 진행률 60%로 갱신. 컨테이너 실기동·UFW 설정은 실 서버 확인 대기 | — |
| 2026-07-02 | v0.0.4 | §8 다음 작업 1번(ERD 최종 확정) 완료 처리 — `backend/docs/ERD.md` 작성. Phase 2 진행률 5%로 갱신, 상태 "진행 중"으로 변경. ERD 정리 중 발견한 미확정 사항 3건을 §9 리스크에 추가 | — |
| 2026-07-02 | v0.0.5 | `HR_EMPL_ROLE_REL` 테이블을 Phase 2 데이터 모델 범위에 포함 확정 (관계자 확인 완료) — 로드맵 전체의 "15개 테이블" 표현을 "16개 테이블"로 정정 (§4 Phase 2/3, §11 데이터베이스·백엔드 체크리스트), §9 해당 리스크 항목 "해결" 처리, `backend/docs/ERD.md`에 §3.6-1 `HR_EMPL_ROLE_REL` 스키마 섹션 추가 | — |
| 2026-07-02 | v0.0.6 | `HR_SKILL_MST` 초기 Seed MVP 초안 작성(55건, 6개 그룹) 및 §9 리스크 "직원 기술 스택 표준화 기준 미정" 상태를 "차단→주의"로 하향 — 운영팀 최종 확정 전까지 MVP 표기 유지, §11 데이터베이스 체크리스트에 항목 추가 (미완료 유지) | — |
| 2026-07-02 | v0.0.7 | `SYS_ROLE_MST` 초기 Seed MVP 확정(ROLE_CD 6종, ROLE_NM/ROLE_DESC/화면 단위 `PERM_JSON`) — `backend/app/db/seed/sys_role_mst_seed.py` 작성, `backend/docs/ERD.md` §3.13 갱신. §9 리스크 "인증/권한 범위 미정", "`SYS_ROLE_MST` 세부 값 미정" 2건 "해결(MVP)"로 처리 | — |
| 2026-07-02 | v0.0.8 | MVP 권한 매트릭스(화면 접근 + 버튼 권한 조회/등록/수정/삭제/Excel/관리자 기능) 작성 — `backend/docs/PERMISSION_MATRIX.md` 신규, `sys_role_mst_seed.py`의 `PERM_JSON`을 화면×버튼 세부 구조(v2)로 갱신. §9 리스크 2건 해결 내용을 v2 매트릭스 기준으로 갱신 | — |
| 2026-07-03 | v0.0.9 | 가동 가능일 MVP 산정 기준 확정 — `backend/docs/AVAILABILITY_CALC_SPEC.md` 신규 작성(기준일/집계조건/`PROPOSED` 제외/3단계 산정식/100% 초과 예외 처리). §9 리스크 "가동 가능일 계산 기준 미정" 상태를 "차단→주의"로 하향, §4 Phase 5·§5 기능별 구현상태·§11 검색추천 체크리스트에 산정 기준 요약 반영 | — |
| 2026-07-03 | v0.1.0 | §8 다음 작업 4번(Alembic `env.py` 설정) 완료 처리 — `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/script.py.mako`, `backend/app/db/base.py` 작성. Phase 2 진행률 5%→10%로 갱신. §11 데이터베이스 체크리스트 "Alembic 마이그레이션 환경 구성" 항목 완료 처리. 실 DB 연결 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v0.1.1 | 전 컨테이너(api/web/worker/db/redis) 타임존 Asia/Seoul(KST) 통일 — `docker-compose.yml`에 `TZ`/`PGTZ` 환경변수 및 `/etc/localtime`·`/etc/timezone` 읽기전용 바인드 마운트 적용(YAML anchor 사용). `[DESIGN]HRM_Automation_System_Design_v0_6.md` §8.3 동일 갱신 및 §8.3-1(타임존 정책/Alpine tzdata 참고/운영 검증 명령) 신규 추가 — 예외적으로 운영 환경 구성 부분만 수정, 업무/DB/화면/API 설계는 변경 없음. §4 Phase 1 작업 목록에 타임존 통일 항목 추가 | — |
| 2026-07-03 | v0.1.2 | §9 리스크 및 차단 이슈 표 구조 변경 — `처리일자` 컬럼 신규 추가. `상태` 열에 섞여 있던 날짜·부가 설명(예: "해결 (MVP, 2026-07-02 갱신)", "주의 (2026-07-03 하향, 기존 차단)")을 `상태`(차단/주의/정상/해소/보류 단일 값)와 `처리일자`(`YYYY-MM-DD` 또는 미처리 시 `-`)로 분리. 상태값 표기를 "해결"→"해소"로 통일(대응 방안 본문 내 동일 표현 포함). 이슈·대응 방안의 실질 내용은 변경하지 않음 | — |
| 2026-07-03 | v0.1.3 | §8 다음 작업 5번(핵심 7개 테이블 생성) 완료 처리 — `backend/app/models/`에 SQLAlchemy 2.x ORM 모델 7종 및 공통 Mixin(`mixins.py`) 신규 작성, Alembic 리비전 `28ce52377e32_create_core_hr_pjt_tables.py` 수기 작성(로컬 `alembic` 패키지 미설치로 autogenerate 불가). Phase 2 진행률 10%→45%로 갱신. §11 데이터베이스 체크리스트에 완료 7개 테이블 체크 표시(전체 16개 중 7개, 부분 완료). 실 DB 적용 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v0.1.4 | §8 다음 작업 6번(`SYS_USER_MST`/`SYS_ROLE_MST`/`SYS_AUDIT_LOG` 테이블 생성 및 Seed 입력) 완료 처리 — 모델 3종 신규 작성, Alembic 리비전 `83fc676b952e_create_sys_user_role_audit_tables.py`(이전 리비전 뒤 체이닝)에 `SYS_ROLE_MST` 6종 Seed(`op.bulk_insert`, 기존 `sys_role_mst_seed.py` 재사용) 포함 작성. Phase 2 진행률 45%→60%로 갱신. §11 데이터베이스 체크리스트에 완료 3개 테이블 체크(전체 16개 중 10개) 및 Seed 항목 부분 완료(HR_JIKGUP_MST/HR_JIKMU_MST Seed 미작성) 반영. 실 DB 적용 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v0.1.5 | §8 다음 작업 7번(사원 목록 조회 API) 완료 처리 — `backend/app/db/session.py`(DB 세션 의존성), `backend/app/schemas/hr_empl_mst.py`, `backend/app/repositories/hr_empl_mst.py`, `backend/app/api/v1/employees.py`, `backend/app/api/v1/router.py` 신규 작성, `backend/app/main.py`에 `/api/v1` 라우터 등록. Phase 3 상태를 "예정→진행 중"(0%→15%)으로 갱신 — 이미 완료돼 있던 FastAPI 기본 구조/`/health`/CORS를 반영. §5 기능별 구현 상태 "직원 관리" 행을 "진행 중(목록 조회만)"으로 갱신, §11 백엔드 체크리스트 3개 항목 완료 체크(FastAPI 구조, `/health`, CORS) 및 사원 CRUD API 부분 완료 명시. 실 서버 기동 기반 엔드포인트 호출 검증은 로컬 환경 제약(`fastapi`/`sqlalchemy` 미설치)으로 미실시 | — |
| 2026-07-03 | v0.1.6 | §8 다음 작업 8번(사원 등록/수정 API) 완료 처리 — `EmployeeCreate`/`EmployeeUpdate` 스키마, `create_employee`/`update_employee`/`get_employee` 리포지토리 함수, `POST`/`PATCH /api/v1/employees` 라우터 추가(UNIQUE/FK 위반 시 409 반환). §4/§5/§11의 "사원 CRUD API" 관련 서술을 "조회/등록/수정 구현, 퇴직 처리 미구현"으로 갱신(Phase 3 진행률은 보수적으로 15% 유지 — 완전한 CRUD 미완성). 실 서버 기동 기반 엔드포인트 호출 검증은 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v0.1.7 | §8 다음 작업 9번(Next.js 기본 레이아웃 구성) 완료 처리 — 기존 로그인/레이아웃/사이드바/상단바 스캐폴딩을 `frontend/lib/auth.ts`(신규, JWT API 전까지 임시 세션 마커)로 실제 동작하는 흐름으로 연결(로그인 시 세션 저장, 미인증 시 `/login` 리다이렉트, 로그아웃 시 세션 제거). Phase 4를 "예정→진행 중"(0%→20%)으로 갱신 — Phase 1에서 이미 완료돼 있던 `output: 'standalone'`/`NEXT_PUBLIC_API_BASE_URL`도 반영. §11 프론트엔드 체크리스트 3개 항목 완료 체크, "공통 레이아웃·네비게이션"은 권한별 메뉴 제어 미구현으로 부분 완료 유지. Next.js 빌드/타입체크는 로컬 환경 제약(Node 16, `node_modules` 미설치)으로 미실시 | — |
| 2026-07-03 | v0.1.8 | §8 다음 작업 10번(사원 목록 화면, 직무 유형 필터) 완료 처리 — `frontend/app/(app)/employees/page.tsx`의 기존 "보유 역할"(하드코딩 목록) 필터를 `HR_JIKMU_MST` 마스터 기반 `jobTypeOptions`("직무 유형")로 교체, 신규/구 코드 혼재 대응 별칭 매핑 추가. Phase 4 진행률 20%→25%로 갱신. §4/§11의 사원 목록 화면 항목 완료 체크(목데이터 기반, 실 API 미연동 명시). Next.js 빌드/타입체크는 로컬 환경 제약으로 미실시 | — |
| 2026-07-03 | v0.1.9 | 실 서버 배포 검증 완료 및 버그 수정 5건 반영 — (1) `frontend/package.json`에 `packageManager` 고정(pnpm 11로 인한 lockfile 충돌 해결), (2) `frontend/public/.gitkeep` 추가(Docker 빌드 COPY 실패 해결), (3) `backend/alembic/env.py`의 `%` 이스케이프 처리(ConfigParser 보간 오류 해결, DATABASE_URL percent-encoding 대응), (4) `backend/app/models/{hr_empl_mst,pjt_mst,pjt_asgn_his}.py` 및 `alembic/versions/28ce52377e32_...py`의 CHECK 제약 6곳에 컬럼명 큰따옴표 추가(Postgres 대소문자 접힘으로 인한 "column does not exist" 오류 해결). 실 서버에서 Docker Compose v2(v5.2.0)·UFW(22/3030/8000)·`alembic upgrade head`(10개 테이블 생성+`SYS_ROLE_MST` 6종 Seed) 전부 정상 동작 확인. §3/§4 Phase 1 진행률 60%→75%로 갱신, §8 4~6번 및 §11 데이터베이스/인프라 체크리스트의 "미검증" 표기를 실 서버 확인 완료로 전환, §9에 `POSTGRES_PASSWORD` 노출 이력(로테이션 필요)·UFW 5442 제한 미확인 리스크 2건 추가 | — |
| 2026-07-03 | v0.2.0 | Phase 1 완료(100%) 처리 — `/health`·포트 3030 curl 응답 정상 확인. `docker-compose.yml`의 `db` 포트 바인딩을 `"5442:5432"` → `"127.0.0.1:5442:5432"`로 변경(UFW 대신 Docker 포트 바인딩 레벨에서 PostgreSQL 외부 노출 차단). `POSTGRES_PASSWORD` 로테이션 완료 확인. §9 리스크 2건(비밀번호 노출, UFW 5442) "해소" 처리, §3/§4 Phase 1을 "완료"로 갱신 | — |
| 2026-07-03 | v0.2.1 | `HR_EMPL_SKILL_REL` 테이블(ERD §3.6) 모델·마이그레이션 신규 작성 — §8 명시 항목 완료 이후 §3/§4 로드맵 순서상 가장 앞선 미완료 Phase(Phase 2)의 다음 순서로 진행. Phase 2 진행률 60%→65%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v0.2.2 | `HR_EMPL_ROLE_REL` 테이블(ERD §3.6-1) 모델·마이그레이션 신규 작성 — 복합 UNIQUE(`EMPL_ID`,`JIKMU_ID`) 제약 포함, `IS_PRIMARY` 정합성 규칙은 서비스 레이어 구현 대상으로 주석 명시. Phase 2 진행률 65%→70%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v0.2.3 | §8 다음 작업 섹션을 Phase 2 잔여 작업 중심 새 큐(0~10번)로 개편, 이미 완료된 항목 0·1은 근거와 함께 완료 처리. `HR_AVAIL_SNAP` 테이블(ERD §3.7) 모델·마이그레이션 신규 작성(`AVAIL_STAT_CD` CHECK 포함, 산정 배치는 Phase 7 별도 구현 예정). Phase 2 진행률 70%→75%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v0.2.4 | §8 다음 작업을 Rolling Backlog(누적 완료 목록이 아닌 다음 작업 큐) 원칙으로 재설정 — 완료된 `HR_EMPL_ROLE_REL`/`HR_AVAIL_SNAP` 항목은 목록에서 제외하고 §7/§11 근거만 남김. Phase 1 마무리 항목은 이미 완료된 사실이 있으나 요청에 따라 0번으로 유지하고 완료 상태로 정확히 표기. 잔여 작업을 `PJT_RSRC_REQ`→`PJT_RCMD_RSLT`→`SYS_BATCH_HIS`→Seed→마이그레이션 체인 점검→실 서버 적용 검증→Phase 2 완료 기준 점검 순으로 재구성 | — |
| 2026-07-03 | v0.2.5 | `PJT_RSRC_REQ` 테이블(ERD §3.10) 모델·마이그레이션 신규 작성 — Rolling Backlog 원칙에 따라 §8에서 완료 항목 제거 및 나머지 재번호(1~6). Phase 2 진행률 75%→80%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v0.2.6 | `PJT_RCMD_RSLT` 테이블(ERD §3.11) 모델·마이그레이션 신규 작성 — §8에서 완료 항목 제거 및 나머지 재번호(1~5). Phase 2 진행률 80%→85%로 갱신, §11 데이터베이스 체크리스트 항목 완료 체크(실 DB 미검증 단서 포함) | — |
| 2026-07-03 | v0.2.7 | `SYS_BATCH_HIS` 테이블(ERD §3.15) 모델·마이그레이션 신규 작성 — ERD 16개 테이블 전체 모델·마이그레이션 작성 완료. 8개 Alembic 리비전이 분기 없는 단일 선형 체인임을 전수 대조로 확인(체인 점검 항목 겸 완료). Phase 2 진행률 85%→90%로 갱신, §8 큐를 Seed/실 서버 검증/Phase2 완료 점검 3개 항목으로 재정리 | — |
| 2026-07-03 | v0.2.8 | `HR_JIKGUP_MST`(10종)/`HR_JIKMU_MST`(12종) Seed 데이터 신규 작성 및 Alembic 리비전(`370c95546556`, head 뒤 체이닝)으로 반영 — 로드맵 §11 Seed 항목 3종(`SYS_ROLE_MST`/`HR_JIKGUP_MST`/`HR_JIKMU_MST`) 전부 완료. Phase 2 진행률 90%→95%로 갱신, §8 큐를 실 서버 검증/Phase2 완료 점검 2개 항목으로 재정리 | — |
| 2026-07-03 | v0.2.9 | **Phase 2 100% 완료** — 실 서버에서 `alembic upgrade head`(7개 리비전 적용), 16개 테이블 생성(`\dt`), Seed 3종 삽입(`SELECT COUNT(*)`), `pg_dump` 백업 파일 생성을 전부 실측 검증 완료. §4/§11의 "실 DB 미검증" 표기 전량을 "실 서버 DB 적용 검증 완료"로 갱신, Phase 2 완료 기준 3개 항목 충족 처리. §8 다음 작업을 Phase 3(FastAPI 백엔드, 20%) 잔여 작업 11개 항목으로 전면 재구성 | — |
| 2026-07-03 | v0.3.0 | 16개 테이블 전체 Pydantic v2 조회(Out) 스키마 작성 완료 — 실 서버 컨테이너 내 실제 임포트 및 ORM 데이터(`PERM_JSON` JSONB, KST 타임존) 검증까지 수행(`novauser` 계정 `docker` 그룹 권한 확인 후 `sg docker`로 직접 접근). `SysUserOut`에서 `ENCR_PWD` 의도적 제외 확인. Phase 3 진행률 20%→28%로 갱신, §8 큐에서 완료 항목 제거 및 재번호(1~9) | — |
| 2026-07-03 | v0.3.1 | 부서/직급/직무 코드 조회 API 구현 — `GET /api/v1/departments`·`/positions`·`/job-types` 신규 라우터·리포지토리 추가, 실 서버에서 `curl`로 실제 응답(10건/12건) 및 `openapi.json` 경로 등록 확인. Phase 3 진행률 28%→33%로 갱신, §11 "부서/직급 코드 API" 완료 체크, "직무 유형 CRUD API"는 조회만 완료로 갱신 | — |
| 2026-07-03 | v0.3.2 | §8 다음 작업 1번(기술 CRUD API) 완료 처리 — `SkillCreate`/`SkillUpdate`, `EmployeeSkillCreate`/`EmployeeSkillUpdate` 스키마 및 리포지토리·라우터(`app/api/v1/skills.py`, `app/api/v1/employee_skills.py`) 신규 작성, `employees.py` 패턴 재사용. 실 서버 재빌드 후 `curl`로 등록/조회/수정 및 422(범위 밖 `PRFCY_LEVL`)/409(FK 위반) 응답 확인. Phase 3 진행률 33%→39%로 갱신, §11 "기술 CRUD API" 완료 체크, §8 큐에서 제거 및 재번호(1~8) | — |
| 2026-07-03 | v0.3.3 | §8 다음 작업 1번(프로젝트 CRUD API) 완료 처리 — `ProjectCreate`/`ProjectUpdate`/`ProjectListResponse` 스키마(`PJT_STAT_CD`는 `PJT_STAT_CODES` 상수 기반 `Literal` 검증) 및 리포지토리·라우터(`app/repositories/pjt_mst.py`, `app/api/v1/projects.py`) 신규 작성, `employees.py`의 skip/limit 페이지네이션 패턴 재사용. 실 서버 재빌드 후 `curl`로 등록/조회/수정, 409(`PJT_CD` 중복), 422(잘못된 상태값), 404(존재하지 않는 ID) 응답 전부 확인. Phase 3 진행률 39%→44%로 갱신, §11 "프로젝트 CRUD API" 완료 체크, §8 큐에서 제거 및 재번호(1~7) | — |
| 2026-07-03 | v0.3.4 | §8 다음 작업 1번(투입 관리 API) 완료 처리 — `AssignmentCreate`/`AssignmentUpdate`/`AssignmentListResponse` 스키마 및 리포지토리·라우터(`app/repositories/pjt_asgn_his.py`, `app/api/v1/assignments.py`) 신규 작성. ERD §3.9/설계서 §5.5의 "동일 사원 동일 기간 ALLOC_RT 합계 100% 초과 금지" 규칙을 `sum_overlapping_alloc_rt` 헬퍼로 구현해 등록/수정 시 409로 거부하도록 적용(집계 대상 상태 MVP 해석은 §9 리스크로 별도 기록). 실 서버 재빌드 후 임시 테스트 데이터로 100%/초과/취소 제외/404 케이스 전부 확인 후 테스트 데이터 삭제. Phase 3 진행률 44%→50%로 갱신, §11 "투입 관리 API" 완료 체크, §9 리스크 1건 추가, §8 큐에서 제거 및 재번호(1~6) | — |
| 2026-07-03 | v0.3.5 | §8 다음 작업 1번(JWT 인증 API) 완료 처리 — `backend/app/core/security.py`(비밀번호 해싱, JWT 발급/검증), `backend/app/schemas/auth.py`, `backend/app/repositories/sys_user_mst.py`, `backend/app/api/v1/auth.py`(`POST /api/v1/auth/{login,refresh,logout}`) 신규 작성. 실 서버 재빌드 중 `passlib[bcrypt]==1.7.4`/`bcrypt>=4.1` 비호환 버그 발견해 `backend/requirements.txt`에 `bcrypt==4.0.1` 고정으로 해결(§9 리스크 기록). 임시 역할·사용자 데이터로 로그인/토큰 갱신/로그아웃 및 401 경로 전부 확인 후 삭제. `.env`의 `JWT_SECRET_KEY`는 이미 설정되어 있어 별도 수정 불필요. Phase 3 진행률 50%→56%로 갱신, §11 "JWT 인증 API" 완료 체크, §9 리스크 2건 추가(로그아웃 무효화 미구현, bcrypt 호환성), §8 큐에서 제거 및 재번호(1~5) | — |
| 2026-07-03 | v0.3.6 | §8 다음 작업 1번(RBAC 권한 미들웨어) 부분 완료 — `backend/app/api/deps.py`(신규, `get_current_user`/`require_permission`) 작성 및 `PERM_JSON` 화면 키가 명확한 5개 라우터(`employees`/`skills`/`employee_skills`/`projects`/`assignments`)에 적용. `codes.py`는 대응 화면 키(`departments`/`positions`) 부재로 적용 보류(§9 리스크 추가) — 항목은 "진행 중"으로 유지, §8 큐에서 제거하지 않음. 실 서버에서 VIEWER/PM 역할 테스트 사용자로 401/403/200/201 경로가 `PERMISSION_MATRIX.md`와 일치함을 확인. Phase 3 진행률은 보수적으로 56% 유지, §11 해당 항목 "진행 중"으로 갱신 | — |
| 2026-07-03 | v0.3.7 | **체크리스트/상태표 정합성 점검(사용자 요청)** — 실 서버 재확인 결과 §11 데이터베이스 체크리스트의 "PostgreSQL Docker 컨테이너 구성"/"바인드 마운트 확인" 2개 항목이 실제로는 Phase 1 완료 시 이미 검증되었음에도 체크 표시가 누락되어 있어 `[x]`로 정정(`docker compose ps` 및 `data/postgres/pgdata` 실존 확인). "Seed 데이터 입력" 항목의 "실 DB 적용 미검증" 문구가 Phase 2 100% 완료 검증(2026-07-03) 이후 갱신되지 않은 것도 발견해 정정. "DB 백업 스크립트+crontab" 항목은 스크립트 작성/수동 실행만 완료(crontab 미완료)임을 명확히 하는 설명을 추가했으나 체크는 보류. "외부 DB 클라이언트 접속 확인" 항목에는 5442 포트가 `127.0.0.1`로만 바인딩되어 있어 문자 그대로의 "외부" 접속은 설계상 불가하다는 점을 주석으로 추가(체크는 보류). 추가로 §5 "기능별 구현 상태"·§6 "기술 구성 요소별 진행 상태" 두 표가 최초 작성 이후 한 번도 갱신되지 않아 이미 완료된 다수 항목(Docker/PostgreSQL/FastAPI/SQLAlchemy/Alembic 등 인프라 전체, 기술/직원기술/프로젝트/투입관리/투입률검증/배포자동화 등 API 기능)이 "예정"으로 남아있던 것을 확인해 실제 상태(완료/진행 중/예정)로 전면 갱신. §3 전체 로드맵 표의 Phase 3 진행률이 33%로 정체되어 있던 것을 §4 상세표 기준 56%로 정정. 실질적인 기능/코드 변경은 없음(문서 정합성 정정만 수행) | — |
| 2026-07-03 | v0.3.8 | §8 다음 작업 2번(`SYS_AUDIT_LOG` 감사 로그 미들웨어) 완료 처리 — `backend/app/repositories/sys_audit_log.py`, `backend/app/core/audit.py`(`record_audit`) 신규 작성. 로그인 및 `employees`/`skills`/`employee_skills`/`projects`/`assignments` 5개 라우터의 등록/수정 엔드포인트에 적용(도메인별 Out 스키마로 변경 전/후 스냅샷 기록). `codes.py`는 RBAC 미적용과 동일하게 제외(§9 참조). 실 서버에서 ADMIN 테스트 사용자로 로그인→등록→수정을 실행해 `SYS_AUDIT_LOG`에 `LOGIN`/`CREATE`/`UPDATE` 3건이 정확히 기록됨을 확인(BFR/AFT JSON 값 일치 포함). Phase 3 진행률 56%→61%로 갱신, §11 "SYS_AUDIT_LOG 감사 로그 미들웨어" 완료 체크, §8 큐에서 제거 및 재번호(1~4) | — |
| 2026-07-03 | v0.3.9 | **RBAC 잔여 범위 완료 — `codes` 공통 코드 권한 신설(운영팀 확인 반영)** — 부서(`departments`)/직급(`positions`)을 독립 화면이 아닌 "공통 코드/기준정보"로 취급하기로 확정(운영팀 확인). `SYS_ROLE_MST.PERM_JSON`에 `codes` 키 신설(`codes.view` 전 역할 허용, `codes.create/update/delete`는 ADMIN/HR_MGR만 허용) — `sys_role_mst_seed.py` Seed 소스 갱신 및 Alembic 리비전 `9c1f3a5d2b7e`(head `370c95546556` 뒤 체이닝, `jsonb_set`으로 기존 DB 행 갱신)로 실 DB 반영. `GET /api/v1/job-types` 조회에도 `codes.view` 정책 병행 적용(관리 화면 등록/수정/삭제는 기존 `job_types.*` A H 전용 유지). `backend/app/api/v1/codes.py` 3개 GET 엔드포인트에 `require_permission("codes", "view")` 적용 — 인증 없이 호출 가능하던 마지막 업무 API 제거. `backend/docs/PERMISSION_MATRIX.md`에 `codes` 권한 섹션 및 화면 키 목록(14종) 갱신. 실 서버에서 `alembic upgrade head` 적용 후 6개 역할 `PERM_JSON` 값 확인, 인증 없이 코드 API 호출 시 401 전환 확인, VIEWER 테스트 사용자로 3개 엔드포인트 정상 조회(200) 확인. Phase 3 진행률 61%→67%로 갱신, §11 "RBAC 권한 미들웨어 구현" 진행 중→완료로 정정, §9 리스크 "departments/positions/job-types 화면 권한 키 미정" 주의→해소 처리(처리일자 2026-07-03) | — |
| 2026-07-03 | v0.4.0 | §8 다음 작업 1번(사원 퇴직 처리 API) 완료 처리 — `backend/app/repositories/hr_empl_mst.py`에 `retire_employee`(신규, `EMPL_STAT_CD='RETIRED'` 전환 + `RETIR_DT` 기록) 추가, `backend/app/api/v1/employees.py`에 `DELETE /api/v1/employees/{empl_id}` 라우터 추가(`retir_dt` 쿼리 파라미터 지원, 기존 `employees.delete` 권한·감사 로그 재사용). 실 서버에서 임시 사원 데이터로 정상 퇴직 전환, 재퇴직 시도 409, 미존재 404, 무인증 401, 권한 없는 역할 403, `SYS_AUDIT_LOG`에 `ACT_CD='DELETE'`(변경 전/후 상태 포함) 기록까지 전부 확인 후 테스트 데이터 삭제. Phase 3 진행률 67%→72%로 갱신, §5·§11 "사원 CRUD API"/"직원 관리" 완료 체크로 정정, §8 큐에서 완료 항목 제거 및 재번호(1~2) | — |
| 2026-07-03 | v0.4.1 | §8 다음 작업 1번(페이지네이션 공통 처리) 완료 처리 — `backend/app/core/pagination.py`(`PaginationParams`), `backend/app/schemas/pagination.py`(`PaginatedResponse[T]` 제네릭) 신규 작성. `EmployeeListResponse`/`ProjectListResponse`/`AssignmentListResponse`를 제네릭 타입 별칭으로 전환(응답 JSON 형태 동일 유지), `employees`/`projects`/`assignments` 3개 라우터의 개별 skip/limit `Query` 선언을 `Depends(PaginationParams)`로 교체. 실 서버 재빌드 후 기본값/커스텀 값/422 검증 범위가 기존과 동일하게 동작함을 확인. `/openapi.json` 스키마명이 `PaginatedResponse_XOut_` 형태로 바뀌는 부수 효과를 §9 리스크로 기록(응답 바디 무영향). Phase 3 진행률 72%→78%로 갱신, §11 "페이지네이션 공통 처리 구현" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1) | — |
| 2026-07-03 | v0.4.2 | §8 다음 작업 1번(OpenAPI 문서 확인) 완료 처리 — 코드 변경 없이 실 서버에서 `/docs`·`/redoc`·`/openapi.json` 정상 응답 및 22개 엔드포인트 태그·설명·응답 코드·`HTTPBearer` 보안 스키마 반영을 확인. Phase 3 진행률 78%→83%로 갱신, §11 "OpenAPI 문서 확인" 완료 체크, §8 큐를 §4 Phase 3 미착수 항목(가동률 계산 API, 대시보드 집계 API, Excel Import/Export API) 3개로 재구성 | — |
| 2026-07-03 | v0.4.3 | §8 다음 작업 1번(가동률 계산 API) 완료 처리 — `backend/app/repositories/hr_avail_snap.py`(`compute_availability`, `AVAILABILITY_CALC_SPEC.md` §2/§4 로직 구현), `backend/app/schemas/hr_avail_snap.py`(`AvailabilityCalcOut`), `backend/app/api/v1/availability.py`(신규, `GET /api/v1/availability/{empl_id}`) 작성. `HR_AVAIL_SNAP` 테이블에 저장하지 않는 즉시 계산 전용 API로 설계(스냅샷 생성 배치는 Phase 7 `HR_AVAIL_SNAP_GEN` 몫으로 이미 문서화되어 있어 중복 구현 회피). 실 서버에서 AVAILABLE/PARTIAL/FULL(종료일 있음)/FULL(데이터 품질 경고)/PROPOSED 제외 5가지 케이스 및 404/401 전부 확인 후 테스트 데이터 삭제. Phase 3 진행률 83%→89%로 갱신, §5 "가동 가능일 자동 계산" 예정→진행 중, §11 "가동률 계산 API" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1~2) | — |
| 2026-07-03 | v0.4.4 | §8 다음 작업 1번(대시보드 집계 API) 완료 처리 — SCR-002 설계서 명시 4개 엔드포인트(`summary`/`dept-utilization`/`job-type-distribution`/`utilization-by-type`) 신규 구현(`app/repositories/dashboard.py`, `app/schemas/dashboard.py`, `app/api/v1/dashboard.py`). `hr_avail_snap.py`에 `active_alloc_rt_subquery` 추출해 가동률 계산 로직 재사용. `HR_AVAIL_SNAP` 배치 미구현으로 실시간 재계산 방식 채택(§9 리스크 기록). 실 서버에서 부서 2개·사원 3명 임시 데이터로 4개 엔드포인트 결과를 수기 계산과 대조해 전부 일치 확인. Phase 3 진행률 89%→94%로 갱신, §11 "대시보드 집계 API" 완료 체크, §8 큐에서 완료 항목 제거 및 재번호(1, Excel Import/Export API만 남음) | — |
| 2026-07-03 | v0.4.5 | 사용자 요청으로 프론트엔드 `/dashboard` 목데이터(`lib/mock-data.ts`) 기준 미구현 위젯 4개 API 추가 — `GET /api/v1/dashboard/{data-quality,ending-this-month,recent-employees,headcount-trend}`. 기존 SCR-002 설계서 명시분(4개)과 합쳐 대시보드 API 총 8개 완성. 임시 사원 3명 데이터로 데이터 품질(기술/직무 미등록, 100% 초과)·이달 종료 예정 상세·최근 입사자(퇴직자 제외)·3개월 인력 추이(입사/퇴사 반영)를 수기 계산과 대조해 전부 검증 완료. §11 "대시보드 집계 API" 항목 설명을 8개 엔드포인트 기준으로 갱신 | — |
| 2026-07-03 | v0.4.6 | 사용자 요청으로 프론트엔드 전체 한글 폰트를 Noto Sans KR로 변경 — `frontend/app/layout.tsx`에서 `Geist`(라틴 전용)를 `Noto_Sans_KR`(subsets `latin`+`korean`)로 교체, `--font-geist-sans` CSS 변수명은 유지해 영향 범위 최소화. `globals.css` 폴백 폰트명 갱신. `docker compose up -d --build web` 재빌드로 TypeScript/Next.js 빌드 정상 통과 확인(로컬 Node 16 제약 대체 검증), 실 서버에서 `font-family: Noto Sans KR` 적용 및 `/login` 정상 렌더링 확인 | — |
| 2026-07-03 | v0.4.7 | §8 다음 작업 1번(Excel Import/Export API) 중 Export만 완료 처리 — SCR-003 컬럼 매핑 그대로 `GET /api/v1/employees/export`(`openpyxl` 신규 의존성) 구현, 보유역할·주요기술·숙련도 N:M 집계 헬퍼 추가. Import는 FK 명칭 조회·upsert·부분 실패 정책 등 설계 판단이 필요해 별도 항목으로 분리(§9 리스크 기록). 실 서버에서 `.xlsx` 실제 내용 검증(10개 컬럼 전부 정확), `excel` 권한 없는 역할 403, 무인증 401, `SYS_AUDIT_LOG` EXPORT 기록 확인. §11 "Excel Import/Export API" 항목을 Export 완료·Import 미구현으로 설명 갱신(체크박스 미완료 유지), §8 큐를 Import 전용 항목으로 재구성 | — |
| 2026-07-03 | v0.4.8 | 사용자 요청으로 백로그 문서에 누락되어 있던 "로그인 JWT API 연동" 항목 신규 추가 — 백엔드 JWT 인증 API는 완료되었으나 프론트엔드가 `lib/auth.ts`의 localStorage 임시 마커 대신 실제 API를 호출하도록 연동하는 작업 자체를 가리키는 백로그 항목이 없었음을 확인해 추가. §4 Phase 4 "주요 작업" 표·§11 프론트엔드 체크리스트에 신규 항목(예정) 추가, §8 다음 작업 큐에 2번 항목으로 등록. 코드 변경 없음(문서 정정만 수행) | — |
| 2026-07-03 | v0.4.9 | §8 다음 작업 2번(로그인 JWT API 연동) 완료 처리 — `frontend/lib/auth.ts`를 localStorage 세션 마커 방식에서 실제 액세스/리프레시 토큰 저장 방식으로 교체(`login`/`logout`/`getAccessToken` 신규, `isAuthenticated` 시그니처 유지). `login/page.tsx`의 목업 로직을 실제 `POST /api/v1/auth/login` 호출로, `top-nav.tsx`의 로그아웃을 실제 `POST /api/v1/auth/logout` 호출로 교체. 토큰 저장은 MVP로 localStorage 유지(HttpOnly Cookie 전환은 백엔드 API 변경 필요해 별도 후속 과제, §9 리스크 기록). 실 서버 컨테이너 재빌드로 TypeScript/Next.js 빌드 통과 확인, 컴파일된 번들에서 `USER_LGID` 로그인 페이로드 실존 확인(브라우저 클릭 테스트는 headless 도구 부재로 미실시). Phase 4 진행률 25%→31%로 갱신, §4/§6/§11 관련 항목 갱신, §9 리스크 1건 추가, §8 큐에서 완료 항목 제거(Excel Import만 남음) | — |
| 2026-07-03 | v0.5.0 | Excel Import 정책 확정 반영: 마스터 미존재 시 전체 실패, `EMPL_NO` 기준 Upsert, 일부 실패 시 전체 롤백 (사용자 확정) — `POST /api/v1/employees/import` 신규 구현(`backend/app/services/employee_import.py`: 파싱·검증·Upsert·역할/기술 동기화, `python-multipart` 신규 의존성). 실 서버에서 정상/마스터 미존재/파일 내 사번 중복/기존 사번 수정 4개 시나리오 및 권한/인증/감사 로그 전부 검증 완료, 실패 시나리오는 DB 무변경 확인. §4 "Excel Import/Export API" 완료 처리, §11 항목 완료 체크. **Phase 3 재점검**: 주요 작업 전 항목 완료로 진행률 100% 갱신했으나, "완료 기준"의 "Pytest 단위 테스트 핵심 API 커버"가 미충족임을 확인해 Phase 3을 "완료"로 선언하지 않음 — §8 다음 작업을 "Pytest 단위 테스트 스위트 구축"으로 재구성, §9 리스크 1건 추가 | — |
| 2026-07-03 | v0.5.1 | **버그 수정** — `NEXT_PUBLIC_API_BASE_URL`이 프론트엔드 Docker 이미지 빌드 시점에 클라이언트 번들로 인라인되지 않던 문제 발견 및 수정(사용자가 프론트엔드 로그인 화면에서 로그인이 안 된다고 보고해 조사 중 발견). `docker-compose.yml`의 `web.build`에 `args: {NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL}}` 추가, `frontend/Dockerfile` builder 스테이지에 `ARG`/`ENV` 선언 추가. Phase 1 때부터 잠재했던 버그로, 화면이 목데이터만 쓰던 동안은 드러나지 않다가 로그인 JWT 연동(v4.9) 이후 처음 실제 영향이 나타남 — 재빌드 후 클라이언트 번들에 백엔드 URL이 정상 포함되고 CORS 프리플라이트·실제 로그인 요청이 브라우저와 동일한 조건(Origin 헤더 포함)으로 정상 동작함을 확인. `.env`/DESIGN 파일은 수정하지 않음. §9 리스크에 "해소"로 기록, §11 관련 항목 설명 갱신 | — |
| 2026-07-03 | v0.5.2 | **Phase 3(FastAPI 백엔드 구축) 정식 완료** — Pytest 단위 테스트 스위트 신규 구축(`backend/tests/`, 16개 테스트: health/인증/RBAC/사원 CRUD/투입관리 ALLOC_RT 검증). 실 DB 연결+SAVEPOINT 격리 패턴으로 테스트 후 자동 롤백되어 DB에 흔적을 남기지 않도록 구현, 실 서버 컨테이너에서 16개 전부 통과 및 잔여 데이터 0건 확인. §4 Phase 3 "완료 기준" 4개 항목 전부 충족되어 개발 상태 "완료"·진행률 100%로 전환, §3 전체 로드맵 갱신, §9 리스크 해소 처리, §8 큐를 Phase 4(Next.js) 잔여 항목으로 재구성 | — |
| 2026-07-03 | v0.5.3 | §8 다음 작업 1번(공통 레이아웃·네비게이션 권한별 메뉴 제어) 완료 처리 — `GET /api/v1/auth/me`(신규, `MeOut` 스키마) 추가해 프론트엔드가 현재 사용자의 `ROLE_CD`/`PERM_JSON`을 조회할 수 있게 함. `frontend/lib/nav.ts`에 `NavItem.permKey` 필드와 `filterNavByPermissions` 헬퍼 추가, `lib/auth.ts`에 `getMe()` 추가, `app-shell.tsx`가 로그인 확인 후 `getMe()` 호출 결과를 `Sidebar`(데스크톱/모바일 공통)에 전달해 메뉴를 화면 권한 기준으로 필터링. `backend/tests/test_auth.py`에 `/auth/me` 테스트 2건 추가(pytest 16→18개 전부 통과). 실 서버에서 `admin` 계정으로 `/auth/me` 정상 응답, 무인증 401, 프론트엔드 재빌드 후 번들에 호출 코드 포함 확인. Phase 4 진행률 31%→38%로 갱신, §4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거(대시보드 화면 구현만 남음) | — |
| 2026-07-03 | v0.5.4 | §8 다음 작업 1번(대시보드 화면 구현) 완료 처리 — `frontend/app/(app)/dashboard/page.tsx`를 목데이터에서 백엔드 대시보드 API 8종 실 호출로 전면 교체. `HeadcountChart`/`JobTypeDonut`/`DeptUtilizationChart` 3개 차트 컴포넌트를 `data` prop 기반으로 리팩터링(소비처인 `reports/page.tsx`도 호환 유지 위해 함께 수정), 인증 API 호출 공통 헬퍼 `frontend/lib/api.ts`(`apiGet<T>`) 신규 작성. 실 서버 재빌드 성공(`/dashboard` 정적 프리렌더, TypeScript 컴파일 오류 없음), 컴파일된 번들에 실 API 호출 코드 포함 확인, `admin` 토큰으로 8개 엔드포인트 전부 직접 호출해 응답 구조가 화면의 TypeScript 인터페이스와 일치함을 확인. Phase 4 진행률 38%→44%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐를 Phase 4 잔여 미완료 항목(사원 상세~설정 화면 등 9개)으로 재구성 | — |
| 2026-07-03 | v0.5.5 | §8 다음 작업 1번(사원 상세 화면 구현) 완료 처리 — 기존 저장소에 이미 있던 목데이터 기반 `/employees/[id]` 프로토타입 화면을 실 API로 연동(기본정보/보유기술/투입이력 3개 탭). 신규 `GET /api/v1/employees/{empl_id}` 백엔드 엔드포인트 추가(기존 `get_employee` 리포지토리 재사용), 기술·투입 이력 조회는 기존 API 그대로 재사용. 정보수정/기술추가/퇴직처리 UI와 "변경 이력" 탭(감사 로그 조회 API 부재)은 후속 작업으로 분리, §9 리스크 4건 추가(편집 UI 미구현·감사 로그 API 부재·부서 마스터 Seed 없음·`hrm-worker` 재시작 루프). `backend/tests/test_employees.py`에 상세 조회 테스트 3건 추가(pytest 18→21개 전부 통과). 실 서버에서 임시 부서·사원 데이터로 상세 조회 200/404, 응답 구조 일치 확인(검증 중 투입 이력 응답이 페이지네이션 래퍼임을 발견해 프론트엔드 파싱 버그 수정). Phase 4 진행률 44%→50%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐 재구성(누락되었던 "설정 화면 구현"·"Excel Import/Export UI 구현" 2개 항목도 함께 추가) | — |
| 2026-07-04 | v0.5.6 | §8 다음 작업 1번(기술 관리 화면 구현) 완료 처리 — 기존 목데이터 기반 `/skills` 화면을 백엔드 `HR_SKILL_MST` API(조회/등록/수정, 이미 구현되어 있어 백엔드 변경 없음)로 연동. `use_yn` 필터 두 상태 병렬 조회로 "전체" 목록 지원, "보유 인원"은 `employee-skills` 전체 조회 결과를 클라이언트에서 집계, "비활성 처리"는 신규 API 없이 기존 `PATCH`의 `USE_YN` 토글로 재사용. `frontend/lib/api.ts`에 `apiPost`/`apiPatch` 공통 헬퍼 신규 추가. 실 서버에서 등록/수정/토글 전부 검증 완료, 검증 중 `SKILL_NM` 유니크 제약 부재(중복 등록 시 오류 미발생)를 발견해 §9 리스크로 신규 기록. 백엔드 변경 없어 pytest는 21개 그대로 유지. Phase 4 진행률 50%→56%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.5.7 | §8 다음 작업 1번(직무 유형 관리 화면 구현) 완료 처리 — 목데이터 기반 `/job-types` 화면을 백엔드 `HR_JIKMU_MST` API로 연동. 기술 관리와 달리 등록/수정 API가 없어 `JobTypeCreate`/`JobTypeUpdate` 스키마, 리포지토리 함수, `POST`/`PATCH /api/v1/job-types`(권한 `job_types.create`/`update`, 감사 로그 연동) 신규 작성. `JIKMU_CD`는 모델에 UNIQUE 제약이 있어 중복 등록 시 409가 정상 반환됨을 확인(직전 턴 `SKILL_NM` 무결성 문제와 대조). `backend/tests/test_codes.py` 신규 작성(5개 케이스, pytest 21→26개 전부 통과). 실 서버에서 등록/중복 409/수정/토글/감사 로그 전부 검증 완료. Phase 4 진행률 56%→63%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.5.8 | **긴급 수정** — 사용자가 SSH 터널로 `localhost:3030` 접속 시 로그인이 "서버에 연결할 수 없습니다" 오류로 실패한다고 보고. 원인은 CORS가 아니라, 빌드 시점에 고정되는 `NEXT_PUBLIC_API_BASE_URL`이 서버의 LAN IP로 절대경로 고정되어 있어 SSH 로컬 포트 포워딩을 우회해 클라이언트 PC가 그 IP로 직접 연결을 시도하다 실패하는 구조였음을 진단(요청이 서버에 도달하기 전에 실패해 `hrm-api` 로그에도 기록이 없음과 일치). `frontend/next.config.mjs`에 `rewrites()` 추가 — `/api/v1/*` 요청을 Next.js 서버가 Docker 내부망의 `api:8000`으로 프록시하도록 구성, 기존 코드가 이미 지원하던 상대 경로 호출 방식과 결합해 코드 변경만으로 LAN IP 직접 접속·SSH 터널(3030 포트만 필요) 두 접속 방식을 하나의 빌드로 동시 지원하도록 구조 개선. 사용자가 `.env`의 `NEXT_PUBLIC_API_BASE_URL`을 빈 값으로 직접 변경(AI는 `.env` 수정 금지 원칙에 따라 값 변경 없이 안내만 제공) 후 재빌드, 번들에서 절대 IP 제거·`curl`로 3030 경유 로그인 200·pytest 26개 그대로 통과 확인. §9 리스크 신규 1건 추가·"해소"로 기록, §8 큐와 무관한 사용자 보고 장애 수정이라 §4 진행률은 변경 없음 | — |
| 2026-07-04 | v0.5.9 | §8 다음 작업 1번(프로젝트 목록/상세 화면 구현) 완료 처리 — 목데이터 기반 `/projects`·`/projects/[id]` 화면을 백엔드 `PJT_MST`/`PJT_ASGN_HIS` API로 연동. 사원 상세와 동일하게 프로젝트 단건 조회 API가 없어 `GET /api/v1/projects/{pjt_id}` 신규 추가. 목록은 `GET /projects` + 진행 중 투입 집계로 투입 인원 컬럼 계산, 등록 모달은 `POST /projects` 실 연동(설계서 목업에 없던 `PJT_CD` 필드는 백엔드 필수값이라 추가, 사유 주석 명시). 상세는 프로젝트 정보 + 투입 이력 + 사원/부서/직무 마스터 조인으로 개요·투입 유형 구성·투입 인력 테이블 실 데이터 렌더링. 수정/종료처리/인력투입 버튼은 사원 상세와 동일한 원칙으로 조회 전용 제공. `backend/tests/test_projects.py` 신규 작성(5개 케이스, pytest 26→31개 전부 통과). 실 서버에서 등록/중복 409/상세조회/404/렌더링 전부 검증 완료. Phase 4 진행률 63%→69%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.6.0 | §8 다음 작업 1번(투입 관리 화면 구현) 완료 처리 — 목데이터 기반 `/assignments` 화면을 백엔드 `PJT_ASGN_HIS` API(이미 완전 구현되어 백엔드 변경 없음)로 연동. 사원/프로젝트 마스터 조인으로 목록 렌더링, 공수 초과 배정 감지 배너를 실 데이터 계산으로 교체. 기존 프로토타입에 없던 "투입 등록" 모달을 설계서(SCR-009) 기준 신규 작성 — 사원/프로젝트 Select, 유형/역할/기간/투입률 입력 후 `POST /assignments` 연동, 100% 초과 시 백엔드 409 메시지를 그대로 표시(예상 투입률 미리보기는 범위 제외). 실 서버에서 60%+50%(합계 110%) 등록 시 409 정상 거부, 페이지 렌더링, 조인 데이터 정상 확인. 백엔드 변경 없어 pytest 31개 그대로 유지. Phase 4 진행률 69%→75%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.6.1 | §8 다음 작업 1번(가동 가능 인력 조회 화면 구현) 완료 처리 — 목데이터 기반 `/availability` 화면을 백엔드 API로 연동. 기존 단건 계산 API(`GET /availability/{empl_id}`)로는 전체 목록 조회가 불가해 `list_availability`(신규, N+1 방지를 위해 전체 투입 이력을 한 번에 조회 후 파이썬에서 집계) 및 `GET /availability`(신규, `jikmu_id`/`dept_id` 필터 지원 — 백로그 명시 "직무 유형 필터" 충족) 추가. 판정 로직을 `_classify` 헬퍼로 추출해 기존 단건 API와 공유(순수 리팩터링, 회귀 위험 최소화). 프론트엔드는 사원/부서/직무/기술 마스터 조인으로 즉시/부분/기간 3개 탭·조직·직무유형·검색 필터를 실 데이터로 구현. `backend/tests/test_availability.py` 신규 작성(4개 케이스, pytest 31→35개 전부 통과). 실 서버에서 즉시/부분 가동 분류, 직무유형 필터, VIEWER 접근 제한 전부 검증 완료. Phase 4 진행률 75%→81%로 갱신, §3/§4/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.6.2 | §8 다음 작업 1번(리소스 추천 화면 구현) 완료 처리 — 백엔드 API가 전혀 없어 추천 알고리즘을 신규 구현: `POST /api/v1/resource-requests`(`PJT_RSRC_REQ` 등록), `POST /api/v1/recommendations/score`(6개 항목 가중 점수 산정 후 `PJT_RCMD_RSLT` 저장 — 직무15%+기술35%+숙련도25%+가동일15%+유사경험7%+역할적합도3%), `GET /api/v1/recommendations/{req_id}`(과거 결과 조회) 추가. 설계서에 항목별 세부 산정 공식이 없어 MVP 해석 적용(§9 리스크 기록), 기존 리스크 "추천 점수 가중치 표기 불일치"는 로드맵 수치로 확정되어 해소. 프론트엔드는 기존 프로토타입을 실 API로 재작성(요건 입력 폼 실 마스터 연동, 결과에 사원명/직무/기술 조인). 다중 기술 선택과 "이 후보로 투입 요청" 버튼은 범위 제외(§9 리스크 기록). `backend/tests/test_recommendations.py` 신규 작성(5개 케이스, pytest 35→40개 전부 통과). 실 서버에서 요청 등록→추천 실행→결과 조회→재실행 시 결과 교체 전부 검증 완료. **Phase 5(리소스 검색 및 추천, 그동안 0%)를 처음으로 진행 상태로 전환**(0%→75%) — 이 참에 지난 턴 이미 완료됐던 "즉시 투입 가능 인력 조회 API"·"가동 가능 인력 화면 구현"이 Phase 5 표에 반영 누락되어 있던 것도 함께 바로잡음. §3/§5/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.6.3 | AI Chat(Phase 6) 착수 전 사전 점검 — 사용자가 `.env`에 DeepSeek LLM 연동 정보(`LLM_PROVIDER`/`DEEPSEEK_API_KEY`/`DEEPSEEK_BASE_URL`/`DEEPSEEK_MODEL_ID`)를 이미 설정했다고 확인. 실행 환경에서 DeepSeek API 실제 인증 호출로 정상 응답을 확인해 네트워크·인증 문제없음을 검증. 사용자가 AI Chat 1차 구현 범위를 "LLM 단순 호출/응답 + 자유 대화형 UI"로 명시적으로 확정하고, 자연어 조건 파싱·SQL 조회 연동·권한 필터링·환각 방지·테스트 질의 검증은 별도 후속 작업으로 분리하기로 결정 — §4 Phase 6 "주요 작업" 표에 이 결정을 반영, §9 리스크 1건 추가(해소 처리, 결정 근거 기록). 코드 변경 없음(사전 점검·백로그 정리만 수행) | — |
| 2026-07-04 | v0.6.4 | 사용자 요청으로 §9에 "9-1. 완료 표시된 화면의 미구현 세부 기능 — 후속 보완 체크리스트" 신규 섹션 추가 — 그동안 §7/§9 곳곳에 흩어져 기록되어 있던 "완료 처리했지만 조회 전용이거나 일부 기능이 빠진" 항목들(사원 관리 목록/상세, 프로젝트 상세, 리소스 추천, 가동 가능 인력, 인증/감사 로그, 기타 백엔드 6개 카테고리 총 13개 세부 항목)을 한 곳에 체크리스트로 통합해 향후 작업 시 누락되지 않도록 정리. 기존 리스크 항목 내용은 변경하지 않고 요약·상호 참조만 추가, 코드 변경 없음(문서 정리만 수행) | — |
| 2026-07-04 | v0.6.5 | §8 다음 작업 1번(AI Chat 화면 구현) 완료 처리 — 사용자 확정 범위(LLM 단순 호출/응답만)로 구현. `backend/app/core/config.py`에 `LLM_PROVIDER`/`DEEPSEEK_*`/`OPENAI_API_KEY` 필드 신규 추가, `.env.example` 동기화(`.env`는 미수정). `backend/app/services/ai_chat.py`(신규) `call_llm`이 `LLM_PROVIDER` 기준 공급자 분기(현재 DeepSeek만 지원, LLM 연동 인터페이스 추상화 항목 충족), `POST /api/v1/ai/chat`(권한 `ai_chat.view`) 신규 추가. 프론트엔드는 기존 목데이터 캔드 응답(SQL·결과 테이블 표시)을 제거하고 실 API 연동으로 교체. 자연어 조건 파싱·SQL 조회 연동·권한 필터링·환각 방지는 §4 Phase 6 표·§9-1 체크리스트에 후속 작업으로 반영. `backend/tests/test_ai_chat.py` 신규 작성(`call_llm` 모킹으로 오프라인 검증, 5개 케이스, pytest 40→45개 전부 통과). 실 서버에서 DeepSeek API 실제 호출로 정상 응답 확인, 무인증 401, 빈 메시지 422, `/ai-chat` 페이지 200 렌더링 확인. Phase 6 진행률 0%→38%로 갱신(그동안 미착수였던 Phase 최초 진행), §3/§4/§5/§11 항목 완료 체크, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.6.6 | §8 다음 작업 1번(리포트 화면 구현) 완료 처리 — 백엔드에 리포트 API가 전혀 없어 신규 구현: `backend/app/repositories/reports.py`의 `build_report`가 기존 대시보드 집계 함수(`get_summary`/`get_dept_utilization`/`get_data_quality`)를 재사용하고 "기술별 인력 분포 Top 10"만 신규 추가, `GET /api/v1/reports/{weekly,monthly}`(설계서상 두 탭이 기간 단위만 다른 동일 구조라 하나의 함수 공유, ISO 주차/YYYYMM 파싱, 권한 `reports.view`) 신규 추가. "월별 가동률 통계" 매트릭스 탭·리포트 발송·Excel 내보내기는 구조 복잡도가 높아 후속 작업으로 분리(§9 리스크 2건 추가). 프론트엔드는 기존 프로토타입의 탭 구성(가동률 매트릭스/인력 추이/기술 분포, 전부 목데이터)을 설계서 기준(주간/월간/월별 통계)으로 재구성, 요약 6개 스탯+부서별 가동률+기술 분포 차트를 실 데이터로 연동. `SkillBarChart` 컴포넌트를 다른 차트와 동일하게 `data` prop 기반으로 리팩터링. `backend/tests/test_reports.py` 신규 작성(6개 케이스, pytest 45→51개 전부 통과). 실 서버에서 신규 사원 등록 시 리포트에 즉시 반영됨을 확인, 잘못된 주차/월 형식 422, `/reports` 페이지 200 렌더링 확인. Phase 4 진행률 81%→88%로 갱신, §3/§4/§11 항목 완료 체크, §9-1 체크리스트에 리포트 후속 항목 3건 추가, §8 큐에서 완료 항목 제거 | — |
| 2026-07-04 | v0.6.7 | 사용자 요청으로 `HR_SKILL_MST` 표준 Seed 재작성 — 기존 MVP 초안(6개 그룹, 55건, DB 미반영)을 사용자 확정 13개 그룹(LANGUAGE/BACKEND/FRONTEND/MOBILE/DB/DATA/INFRA/SECURITY/ARCHITECTURE/QA/CONSULTING/PMO/BUSINESS) 110건으로 전면 교체, Excel Import "주요기술" 컬럼 매핑을 고려한 표준 영문/일반 명칭 사용. Alembic 마이그레이션 `55106956dedf`(신규)로 `(SKILL_GRP_CD,SKILL_NM)` 복합 UNIQUE 제약 추가 + `INSERT ... ON CONFLICT DO NOTHING`으로 멱등 반영, 이 제약 추가로 기존 §9 리스크 "`SKILL_NM` 유니크 제약 없음"도 함께 해소. 실 서버에서 `alembic upgrade head`/`downgrade -1`/재`upgrade` 전부 실행해 110건 정상 반영·복원 확인(멱등성 검증), API 레벨 중복 등록 시 409 재확인. `backend/tests/test_skills.py` 신규 작성(4개 케이스, pytest 51→55개 전부 통과). §9 리스크 2건 해소, §11 데이터베이스 체크리스트 항목 완료 체크 | — |
| 2026-07-04 | v0.6.8 | 사용자 질의("검색 필터가 DB에서 조회되는지, 하드코딩인지")로 전 화면 필터 데이터 소스 감사 — `HR_SKILL_MST` 표준 Seed 재작성(v6.7) 직후라 **기술 관리(`/skills`) 화면의 "기술 그룹" 필터가 `lib/options.ts`에 하드코딩된 옛 7개 그룹**을 그대로 사용 중이라 새 Seed의 13개 그룹 중 다수가 필터로 선택 불가능한 버그를 발견 — 즉시 수정: 하드코딩된 `skillGroupOptions`를 제거하고 화면에서 실제로 불러온 데이터의 `SKILL_GRP_CD` distinct 값으로 필터·등록 모달 그룹 목록을 동적 생성. 직무 유형(`/job-types`) 화면의 "그룹" 필터도 동일한 방식으로 실 데이터 기반으로 전환하되, 등록/수정 모달은 설계서(SCR-006)가 명시한 고정 3종(TECHNICAL/MANAGEMENT/ANALYSIS)을 그대로 유지(신규 등록 시 그룹명 난립 방지 목적, 필터와 별개 문제이므로 분리 유지). 감사 결과 나머지 화면(가동 가능 인력·리소스 추천의 조직/직무유형/기술 필터)은 이미 실 API 기반, 상태/유형 계열 필터는 DB CHECK 제약과 동일한 고정 열거값이라 하드코딩이 정상 설계임을 확인. 재빌드 후 `/skills`·`/job-types` 페이지 200 렌더링, pytest 55개 그대로 통과(백엔드 변경 없음) 확인. §9 리스크 1건 추가(해소 처리, 발견·수정 내용 기록) | — |
| 2026-07-04 | v0.6.9 | §8 다음 작업 1번(설정 화면 구현) 완료 처리 — 기존 `/settings` 화면(사용자관리/감사로그 탭 UI는 이미 완성, 전부 목데이터)을 백엔드 실 API로 연동. 백엔드 API가 전혀 없어 신규 구현: `GET/POST /api/v1/users`(등록 시 비밀번호 정책 검증 + 해시 저장), `GET /api/v1/users/roles`(역할 드롭다운용, `SYS_ROLE_MST` 목록 API 자체가 없어 신규), `GET /api/v1/audit-logs`(`SYS_USER_MST` 조인, 사용자/행위/테이블/기간 필터). 계정 수정·비활성화, 감사 로그 Excel 내보내기, `tgt_id` 단건 필터는 후속 작업으로 분리(§9 리스크 3건 추가), 기존 리스크 "사원 상세 '변경 이력' 탭 미구현"도 "API는 확보, tgt_id 필터+화면 연동 남음"으로 부분 해소 갱신. `backend/tests/test_users.py`·`test_audit_logs.py` 신규 작성(8개 케이스, pytest 55→63개 전부 통과). 실 서버에서 사용자 등록/약한 비밀번호 422/중복 409, 감사 로그 조회/필터 전부 검증 완료. Phase 4 진행률 88%→94%로 갱신, §3/§4/§11/§9-1 항목 갱신, §8 큐에서 완료 항목 제거(Excel Import/Export UI만 남음) | — |
| 2026-07-04 | v0.7.0 | §8 다음 작업 1번(Excel Import/Export UI 구현) 완료 처리 — §8 큐 마지막 항목. 사원 목록 화면(`/employees`)에 "Excel 가져오기/내보내기" 버튼 신규 추가, 기존 백엔드 `GET/POST /api/v1/employees/{export,import}` API에 연동(`frontend/lib/api.ts`에 `apiUploadFile`/`apiDownloadFile` 헬퍼 및 `ApiError.detail` 필드 신규 추가, `components/employees/employee-import-dialog.tsx` 신규). **검증 중 실제 라우팅 버그 발견**: `GET /export`가 `GET /{empl_id}`(UUID 경로) 라우트보다 뒤에 등록되어 있어 "export"가 UUID 파싱 실패로 항상 422를 반환하던, 한 번도 정상 동작한 적 없던 기존 버그 — 라우트 등록 순서를 수정해 해결, `backend/tests/test_employees_excel.py` 신규 작성(회귀 방지 2개 케이스, pytest 63→65개 전부 통과). 사원 목록 화면 자체는 여전히 목데이터 기반이라 Import 성공 후 화면 목록은 갱신되지 않음(기존 §9-1 리스크와 동일 사안, 신규 아님). Phase 4 진행률 94%→100%로 갱신(Phase 4 전체 완료), §3/§4/§9/§11 항목 갱신, §8 큐가 이번 항목 제거로 완전히 소진(빈 큐) — 다음 라운드는 Phase 5(75%) 잔여 항목 또는 §9-1 후속 보완 체크리스트 중에서 우선순위 재확정 필요 | — |
| 2026-07-04 | v0.7.1 | §8 다음 작업 1번(직무 유형·기술·숙련도 복합 필터 검색 API 구현) 완료 처리 — `GET /api/v1/availability`에 `skill_id`/`min_prfcy_levl` 쿼리 파라미터 신규 추가, `list_availability` 리포지토리 함수가 `HR_EMPL_SKILL_REL` 조건을 서브쿼리로 결합해 기존 직무 유형·부서 필터와 복합 적용(N+1 방지 구조는 그대로 유지). 프론트엔드 화면은 이미 클라이언트 측 기술명 검색을 지원해 이번 범위에서는 변경하지 않음(최소 단위 원칙). `backend/tests/test_availability.py`에 필터 케이스 1개 추가(pytest 65→66개 전부 통과), 실 서버 HTTP 호출로 기술·숙련도 조건 필터링 정상 동작 확인. Phase 5 진행률 75%→88%로 갱신(8개 중 7개 완료), §3/§4/§11 항목 갱신, §8 큐를 Phase 6 "자연어 조건 파싱 구현"으로 재구성(사용자 이전 확정에 따라 착수 전 범위 재확인 권장) | — |
| 2026-07-04 | v0.7.2 | 사용자 승인으로 §8 다음 작업 1번(자연어 조건 파싱 구현, Phase 6) 완료 처리 — 범위를 파싱으로만 제한(사용자 지시). `backend/app/services/ai_parser.py`(신규) — LLM 미사용, 마스터 데이터 매칭(직무 유형/기술/부서, 기존 repository 재사용)+정규식(가동일·기간, 숙련도)만으로 규칙 기반 파싱, `backend/app/schemas/ai_chat.py`에 `ParsedResourceQuery` 표준 스키마 추가. SQL 조회·권한 필터링·환각 방지는 이번 범위에서 구현하지 않되 모듈 경계는 분리해둠. `backend/tests/test_ai_parser.py`(신규, 12개 케이스 — 사용자 제시 10개 예시 전부 포함) 작성, pytest 66→78개 전부 통과. Phase 6 진행률 38%→50%로 갱신, §3/§4/§9-1/§11 항목 갱신, §8 큐를 사용자가 순차 진행을 확정한 "파싱 결과 → SQL 조회 → 결과 요약 흐름 구현"으로 재구성(whitelist 기반 intent + 기존 repository/query builder만 사용, free-form SQL 생성·실행 금지) | — |
| 2026-07-04 | v0.7.3 | §8 다음 작업 1번(파싱 결과 → SQL 조회 → 결과 요약 흐름 구현, Phase 6) 완료 처리 — `backend/app/services/ai_resource_search.py`(신규) `search_resources`가 whitelist(`intent="resource_search"`) 기반으로 기존 `list_availability` repository만 재사용해 조회(LLM 미관여, free-form SQL 없음), `backend/app/repositories/hr_empl_mst.py`에 `list_employees_by_ids` 추가. `POST /api/v1/ai/chat`을 갱신해 조건 인식 시 LLM 없이 결정적 요약 응답, 그 외는 기존 LLM 경로 유지(회귀 없음). 다중 기술은 1개까지만 조회 반영(`skipped_skills`로 안내), 권한 필터링·환각 방지는 미구현으로 남겨 §9 리스크 신규 추가(AI Chat 조회 결과 권한 필터링 미적용, 영향도 중간). `backend/tests/test_ai_resource_search.py`(4개), `test_ai_chat.py`(1개 추가) 작성, pytest 78→83개 전부 통과. Phase 6 진행률 50%→63%로 갱신(8개 중 5개 완료), §3/§4/§9/§9-1/§11 항목 갱신, §8 큐를 "권한 필터링 후 LLM 컨텍스트 전달 구현"으로 재구성 | — |
| 2026-07-04 | v0.7.4 | 사용자 요청으로 DB 목데이터 생성 스크립트 추가(§8 큐 항목 아님) — `backend/app/db/mock/load_mock_data.py`(신규), `reference/ResourceManagement_v2.xlsx` 형식 기준 사원 30명·프로젝트 12건(실제 금융회사 고객사명)·투입 이력 30건 생성, 재실행 안전(멱등). 검증 중 `search_resources`가 마스터 데이터에 없는 조건을 조용히 무시하던 버그를 발견해 즉시 빈 결과 반환하도록 수정. pytest 83개 전부 통과(회귀 없음) | — |
| 2026-07-04 | v0.7.5 | 사용자 요청으로 사원 목록 화면(`/employees`) 실 API 연동 + 목데이터 정리 스크립트 추가 — `/projects`는 이미 실 API 연동 상태임을 확인(작업 불필요). `frontend/app/(app)/employees/page.tsx`를 `GET /api/v1/employees`+`departments`/`positions`/`job-types`/`availability` 조인 방식으로 전면 재작성, "보유 역할" 표시용 `GET /api/v1/employee-roles`(신규, `backend/app/repositories/hr_empl_role_rel.py`+`api/v1/employee_roles.py`) 추가, 필터를 실 마스터 데이터 기준 동적 생성으로 전환. "사원 등록" 모달은 여전히 API 미연결 스텁으로 후속 과제 유지. `backend/tests/test_employee_roles.py`(2개) 작성, pytest 83→85개 전부 통과. `backend/app/db/mock/remove_mock_data.py`(신규) — `load_mock_data.py`의 데이터 정의를 그대로 재사용해 이 스크립트가 넣은 사원/프로젝트/투입이력/역할/기술 연결만 정확히 삭제(부서는 운영 마스터로 보존), 실 서버에서 제거→재실행(멱등 확인)→재적재까지 실행 검증 완료 | — |
| 2026-07-04 | v0.7.6 | 사용자 신고로 사원 상세·리포트 화면 크래시 2건 수정 — (1) `frontend/app/(app)/employees/[id]/page.tsx`가 `GET /api/v1/projects`를 배열로 잘못 취급해(`ProjectOut[]`) `projects.map is not a function` 크래시 발생 → 실제 응답 형태(`{total, items}`)에 맞춰 `ProjectListResponse` 타입과 `.items` 사용으로 수정. (2) `frontend/app/(app)/reports/page.tsx`의 `StatCard tone="danger"`가 `components/common/stat-card.tsx`에 정의되지 않은 값이라 `toneStyles["danger"]`가 `undefined`가 되어 크래시 → `StatCard`에 `danger` 톤을 정식 추가. `next.config.mjs`의 `typescript.ignoreBuildErrors: true`로 인해 두 타입 오류 모두 빌드 시점에 걸러지지 않고 런타임까지 통과했던 것이 근본 원인 — 같은 패턴(`tone=`/`variant=` 오기입) 전수 검색해 추가 발견 없음 확인. 백엔드 변경 없음, pytest 85개 그대로 통과, 재빌드 후 두 페이지 200 렌더링 확인 | — |
| 2026-07-04 | v0.7.7 | 사용자 요청으로 리포트 화면 탭 순서를 "매트릭스/주간/월간"으로 변경(초기 탭도 매트릭스)하고, 그동안 "준비 중"이던 "월별 가동률 통계" 매트릭스를 실제로 구현 — `backend/app/repositories/reports.py`의 `build_utilization_matrix`가 `PJT_ASGN_HIS`를 월별로 재계산해 사원별 소계/연평균/100% 초과 월과 조직 평균 3단계(수행중만/+투입준비중/전체)를 산출, `GET /api/v1/reports/utilization-matrix` 신규 추가. 프론트엔드는 기존 목데이터 프로토타입(`components/reports/utilization-matrix.tsx`)을 실 API 연동으로 교체, 기간·부서 필터와 100% 초과 강조 포함. `backend/tests/test_reports.py` 3개 케이스 추가, pytest 85→88개 전부 통과. 현재 DB 목데이터 기준 curl로 실제 조회 결과 확인(조직 평균 가동률 16.7%→73.3% 추세 확인) | — |
| 2026-07-04 | v0.7.8 | 사용자 요청으로 사이드바·톱내비 로고 교체 — 사이드바 아이콘+텍스트 로고를 `Blueward-CI_Inverse.png`(150×27px)로 교체, 톱내비의 미연동 "전역 검색" 입력창을 제거하고 사이드바에서 제거한 기존 아이콘 로고(`Boxes` 아이콘 박스)+"HRM 자동화 시스템(Resource Mgmt)" 텍스트로 대체(최초 구현 시 CI 이미지를 잘못 넣었던 것을 사용자 피드백으로 정정). 이미지 파일을 `frontend/public/`로 위치(Next.js 정적 자산 규칙). 백엔드 변경 없음, pytest 88개 그대로 통과 | — |
| 2026-07-04 | v0.7.9 | 사용자 요청으로 인력·투입 목데이터 조정 — `backend/app/db/mock/load_mock_data.py` 데이터 정의 수정: "영업" 조직 인원을 5명→2명으로 축소(3명은 "세일즈파트너"로 이동), 잔류 2명은 투입 이력을 전부 제거해 가동률 0%로 조정, 2·9·18번 사원을 "2025년 A프로젝트 → 2026년 각기 다른 프로젝트" 연간 로테이션으로 재구성, 11·12·13·14번 사원에 3~5개월 겹치는 투입을 추가해 120% 초과 상태로 조정. `remove_mock_data`→`load_mock_data` 재실행으로 실 DB 반영, `GET /availability`·`GET /reports/utilization-matrix` 조회로 조정 결과 실측 검증. 백엔드/프론트엔드 코드 변경 없음(데이터 정의만 수정), pytest 88개 그대로 통과 | — |
| 2026-07-04 | v0.8.0 | 사용자 요청으로 월별 가동률 통계 표의 "사원" 정보를 사원 그룹당 1회만 표시하도록 개선 — `components/reports/utilization-matrix.tsx`를 "사원"/"프로젝트" 2컬럼으로 분리하고 사원 정보 셀을 `rowSpan`으로 병합. 백엔드 변경 없음, pytest 88개 그대로 통과 | — |
| 2026-07-04 | v0.8.1 | §8 다음 작업 1번(권한 필터링 후 LLM 컨텍스트 전달 구현, Phase 6) 완료 처리 — `POST /api/v1/ai/chat`이 `resource_search` 응답 전 요청자 `PERM_JSON`의 `availability.view` 권한을 확인하도록 수정, 권한 없으면 조회 미실행+안내 메시지 반환. `app/api/deps.py`에 `has_permission` 유틸 신규 추가(`require_permission`과 로직 공유, 기존 동작 변경 없음). 부서 등 행 단위 세부 범위 제한은 기존 권한 모델의 한계로 이번 범위에서도 제외(화면 단위까지만). `backend/tests/test_ai_chat.py`에 VIEWER 차단 케이스 추가, pytest 88개 전부 통과. Phase 6 진행률 63%→75%로 갱신(8개 중 6개 완료), §3/§4/§9/§9-1/§11 항목 갱신(§9 리스크 해소), §8 큐를 "환각 방지 시스템 프롬프트 적용"으로 재구성 | — |
| 2026-07-04 | v0.8.2 | §8 다음 작업 1번(환각 방지 시스템 프롬프트 적용, Phase 6) 완료 처리 — `app/services/ai_chat.py`의 `call_llm`이 매 호출 시 시스템 메시지로 환각 방지 프롬프트를 함께 전달(DB 미조회 상태에서 구체적 HR 데이터를 지어내지 말고 시스템 조회 기능 사용을 안내하도록 지침). `backend/tests/test_ai_chat_service.py` 신규 작성(1개 케이스, `httpx.post` 모킹), pytest 88→90개 전부 통과. Phase 6 진행률 75%→88%로 갱신(8개 중 7개 완료), §3/§4/§9-1/§11 항목 갱신, §8 큐를 "테스트 질의 10개 이상 검증"으로 재구성(완료 시 Phase 6 100%) | — |
| 2026-07-04 | v0.8.3 | §8 다음 작업 1번(테스트 질의 10개 이상 검증, Phase 6) 완료 처리 — `backend/tests/test_ai_chat_e2e.py`(신규)로 사용자 확정 예시 질의 10개를 `POST /api/v1/ai/chat` 전체 경로 기준 검증(전부 LLM 미경유, 결정적 요약 반환 확인), 일반 대화 LLM 폴백 회귀 케이스 1건 추가. 검증 중 응답 문구 "가동률"이 실제로는 "가동 가능률"(`AVAIL_RT`)을 가리켜 의미가 반대인 표기 오류를 발견해 수정. pytest 90→101개 전부 통과. **Phase 6(AI 질의응답 연동) 8개 항목 전부 완료, 진행률 88%→100%, 상태 "진행 중→완료"** — §3/§4/§5/§11 항목 갱신, §8 큐를 Phase 7 "HR_AVAIL_SNAP_GEN 배치 구현"으로 재구성 | — |
| 2026-07-04 | v0.8.4 | §8 다음 작업 1번(`HR_AVAIL_SNAP_GEN` 배치 구현, Phase 7) 완료 처리 — `backend/app/repositories/hr_avail_snap.py`에 `generate_avail_snap`(스냅샷 저장+재실행 안전) 신규 추가, `backend/app/services/avail_snap_gen.py`(신규) `run_avail_snap_gen`이 `SYS_BATCH_HIS`에 실행 이력 기록, `backend/app/worker.py`를 APScheduler `BlockingScheduler`(KST 매일 01:00)로 교체(기존 `print` 자리표시자 대체). `requirements.txt`에 `apscheduler==3.10.4` 추가. 실 서버 `worker` 컨테이너에서 스케줄러 기동·배치 수동 실행·멱등성 전부 확인(목데이터 30명 기준 스냅샷 30건 생성). `backend/tests/test_avail_snap_gen.py`(2개) 작성, pytest 101→103개 전부 통과. 대시보드·리포트 API는 여전히 스냅샷 미조회(§9 기존 리스크 유지). Phase 5 마지막 항목도 함께 완료되어 Phase 5 100%, Phase 7 0%→10%로 갱신, §3/§4/§5/§9-1/§11 항목 갱신, §8 큐를 "PJT_ASGN_END_ALERT 배치 구현"으로 재구성 | — |
| 2026-07-04 | v0.8.5 | §8 다음 작업 1번(`PJT_ASGN_END_ALERT` 배치 구현, Phase 7) 완료 처리 — `backend/app/repositories/pjt_asgn_his.py`에 `list_ending_soon_assignments` 추가, `backend/app/services/teams_notify.py`(신규, Teams Webhook 미설정 시 조용히 건너뜀)와 `backend/app/services/asgn_end_alert.py`(신규, `run_asgn_end_alert`가 `SYS_BATCH_HIS` 이력 기록) 구현, `app/core/config.py`에 `TEAMS_WEBHOOK_URL` 필드 추가, `app/worker.py`에 매주 금 17:00(KST) cron 등록. 실 서버 `worker` 컨테이너에서 스케줄러 등록·배치 수동 실행·목데이터 대상 종료 예정 건수 정상 판별 확인. `backend/tests/test_asgn_end_alert.py`(2개, 실행 전/후 비교 방식) 작성, pytest 103→105개 전부 통과. `TEAMS_WEBHOOK_URL` 미설정으로 실제 알림 전송은 미검증(§9 리스크 신규). Phase 7 진행률 10%→20%로 갱신, §4/§5/§9/§11 항목 갱신, §8 큐를 "HR_DATA_QUALITY_CHK 배치 구현"으로 재구성 | — |
| 2026-07-04 | v0.8.6 | 사용자 지시로 §9-1 체크리스트 순서 기준 작업 진행 — 첫 미완료 항목 "사원 목록 '사원 등록' 모달 API 미연결" 처리. `frontend/components/employees/employee-form-modal.tsx`를 실 API(`POST /api/v1/employees`) 연동으로 재작성, 조직/직급 Select를 부모가 조회해둔 실 마스터 데이터로 교체, 등록 성공 시 목록 자동 새로고침 연결. 목데이터 타입 기준이던 미사용 `employee`/`isEdit` prop은 제거(수정 모드는 사원 상세 "정보수정" 버튼 자체가 없어 별도 후속 작업). 백엔드 변경 없음(기존 API 재사용), pytest 105개 그대로 통과, 실 서버에서 curl로 등록 정상 동작 확인. §9-1 해당 항목 `[x]` 처리 | — |
| 2026-07-04 | v0.8.7 | §9-1 다음 미완료 항목 "사원 상세 화면 정보수정 버튼/폼 없음" 처리 — `employee-form-modal.tsx`에 `employee` prop 기반 수정 모드(`PATCH /api/v1/employees/{empl_id}`) 재도입, 등록/수정 양쪽에서 동일 컴포넌트 재사용(사번은 수정 불가). `employees/[id]/page.tsx`에 "정보수정" 버튼 추가, `loadEmployeeDetail`이 이미 조회하던 `departments`/`positions`를 재사용해 모달에 전달, 저장 후 상세 데이터 재조회. 백엔드 변경 없음, pytest 105개 그대로 통과, 실 서버 curl로 PATCH 정상 동작 확인(검증 후 원복). §9-1 해당 항목 `[x]` 처리 | — |
| 2026-07-04 | v0.8.8 | §9-1 다음 미완료 항목 "사원 상세 화면 기술추가 버튼/폼 없음" 처리 — `components/employees/employee-skill-form-modal.tsx`(신규) 작성, 백엔드 `POST /api/v1/employee-skills`(기존 구현) 연동. 기술 Select는 사원 상세 화면이 이미 조회해둔 전체 기술 목록(`skillCatalog`로 반환값에 노출)에서 이미 보유한 기술을 제외해 중복 등록(409) 사전 방지, 숙련도(1~5)·경력(년)·최근 사용일 입력 지원. "보유 기술" 탭에 "기술 추가" 버튼 추가, 저장 후 재조회. 기존 기술 항목 수정은 범위 밖(별도 후속). 백엔드 변경 없음, pytest 105개 그대로 통과, 실 서버 curl로 등록 정상 동작 확인(검증 후 삭제). §9-1 해당 항목 `[x]` 처리 | — |
| 2026-07-04 | v0.8.9 | 사용자 요청("사원정보 중 직무 유형을 수정하려면?" → "지정할 수 잇게 고쳐줘") 처리 — 등록/수정 공용 `employee-form-modal.tsx`에 "직무 유형" Select 필드 추가(호출부가 이미 조회해둔 `job-types` 마스터 데이터 재사용, "선택 안 함" 옵션으로 `JIKMU_ID: null` 지정 가능). `employees/page.tsx`(등록 모달)·`employees/[id]/page.tsx`(정보수정 모달, `loadEmployeeDetail`이 이미 조회하던 `jobTypes` 배열을 반환값에 노출)에 새 prop 전달 배선. 백엔드 `EmployeeCreate`/`EmployeeUpdate` 스키마가 이미 `JIKMU_ID`를 지원하고 있어 백엔드 변경 없음, pytest 105개 그대로 통과. §9-1 정식 체크리스트 항목은 아닌 사용자 직접 요청 건 | — |
| 2026-07-04 | v0.8.10 | 사용자 리포트 버그 수정 — "직무 유형을 컨설턴트→영업으로 바꿨는데 사원 목록 '보유 역할'이 그대로다". 원인: 목록의 "보유 역할" 배지는 `HR_EMPL_MST.JIKMU_ID`가 아니라 별도 N:M 테이블 `HR_EMPL_ROLE_REL`(엑셀 임포트/목데이터로만 채워짐)을 조회하는데, `PATCH /api/v1/employees/{empl_id}`가 `JIKMU_ID`만 갱신하고 이 테이블의 `IS_PRIMARY=TRUE` 행은 그대로 둬서 옛 직무 유형이 계속 표시됨(모델 docstring이 명시한 "IS_PRIMARY 행의 JIKMU_ID는 HR_EMPL_MST.JIKMU_ID와 일치해야 한다" 규칙이 실제로는 지켜지지 않고 있었음). `backend/app/repositories/hr_empl_mst.py`의 `update_employee`에 `_sync_primary_role` 신규 추가 — `JIKMU_ID` 변경 시 기존 `IS_PRIMARY` 행을 새 값으로 갱신(비주 역할로 이미 존재하면 그 행을 주 역할로 승격, UNIQUE(EMPL_ID,JIKMU_ID) 위반 방지), `JIKMU_ID`를 `null`로 바꾸면 주 역할 행 삭제. `backend/tests/test_employee_roles.py`에 회귀 테스트 1건 추가, pytest 105→106개 전부 통과. **데이터 정정**: 이번 버그로 어긋나 있던 사원 2명(양지호 BW-024, 손예준 BW-025)의 `HR_EMPL_ROLE_REL` 주 역할 행을 컨설턴트→영업으로 직접 정정(운영 DB, 실 서버 컨테이너에서 API로 확인). 다른 사원의 유사 불일치 여부는 이번 검증 범위에서는 확인하지 않음(§9 리스크로 기록) | — |
| 2026-07-04 | v0.8.11 | §9-1 다음 미완료 항목 "사원 상세 화면 퇴직처리 버튼 없음" 처리 — 백엔드 `DELETE /api/v1/employees/{empl_id}`(기존 구현, 소프트 삭제)에 프론트엔드 연동 추가. `lib/api.ts`에 `apiDelete` 헬퍼 신규, 기존에 어느 화면에서도 쓰이지 않던 공용 `ConfirmDialog` 컴포넌트를 처음 연결해 "퇴직처리" 버튼 클릭 시 확인 후 호출, 이미 퇴직 처리된 사원은 버튼 비활성화. 백엔드 변경 없음, pytest 106개 그대로 통과, 실 서버 curl로 `ACTIVE→RETIRED` 전환·재요청 409 확인(검증용 임시 사원은 삭제). §9-1 "사원 상세 화면 퇴직처리 버튼" 항목 및 관련 §9 리스크(정보수정·기술추가·퇴직처리 UI 미구현) `[x]`/"해소" 처리 | — |
| 2026-07-05 | v0.8.12 | §9-1 다음 미완료 항목 "사원 상세 화면 '변경 이력' 탭 미구현" 처리 — `GET /api/v1/audit-logs`에 `tgt_id` 필터 신규 추가(`sys_audit_log.py` 리포지토리/라우터), 사원 상세 화면에 "변경 이력" 탭 UI 연동(`tgt_tbl_nm=HR_EMPL_MST&tgt_id={empl_id}`). `settings_audit_logs.view` 권한이 Admin 전용이라 탭 클릭 시에만 지연 조회하고 403은 화면 에러가 아니라 탭 내부 안내로 별도 처리. `backend/tests/test_audit_logs.py`에 `tgt_id` 필터 회귀 테스트 1건 추가, pytest 106→107개 전부 통과. 실 서버 curl로 특정 사원 필터 시 다른 사원 로그와 섞이지 않음을 확인, `/employees/{empl_id}` 페이지 200 렌더링 확인. §9-1 "사원 상세 화면 변경 이력 탭" 항목 및 관련 §9 리스크(감사 로그 조회 API 부재) `[x]`/"해소" 처리 | — |
| 2026-07-05 | v0.8.13 | §9-1 다음 미완료 항목 "프로젝트 상세 화면 수정 버튼/폼 없음" 처리 — 그동안 목데이터 기반으로 미사용 상태이던 `components/projects/project-form-modal.tsx`를 실 API 연동 공용 컴포넌트로 교체(사원 관리의 `employee-form-modal.tsx`와 동일한 `project` prop 기반 등록/수정 공용 패턴), `projects/page.tsx`의 인라인 등록 모달을 이 공용 컴포넌트로 대체, `projects/[id]/page.tsx`에 "수정" 버튼 추가. 프로젝트 코드는 수정 불가(UNIQUE 제약). 백엔드 변경 없음, pytest 107개 그대로 통과, 실 서버 curl로 `PATCH` 정상 동작 확인(검증용 임시 프로젝트는 삭제). §9-1 "프로젝트 상세 화면 수정 버튼/폼" 항목 `[x]` 처리(종료처리·인력투입 버튼은 미완료 유지) | — |
| 2026-07-05 | v0.8.14 | §9-1 다음 미완료 항목 "프로젝트 상세 화면 종료처리 버튼 없음" 처리 — 사원 상세 화면의 "퇴직처리"와 동일한 패턴으로 공용 `ConfirmDialog`를 재사용해 "종료처리" 버튼 클릭 시 확인 후 `PATCH /api/v1/projects/{pjt_id}`(`PJT_STAT_CD: 'CLOSED'`)만 호출. 이미 종료된 프로젝트는 버튼 비활성화. 백엔드 변경 없음(기존 `PATCH` API 재사용), pytest 107개 그대로 통과, 실 서버 curl로 `PJT_STAT_CD` 정상 전환 확인(검증용 임시 프로젝트는 삭제). §9-1 "프로젝트 상세 화면 종료처리 버튼" 항목 `[x]` 처리(인력투입 버튼은 미완료 유지) | — |
| 2026-07-05 | v0.8.15 | §9-1 다음 미완료 항목 "프로젝트 상세 화면 인력투입 버튼 없음" 처리 — 그동안 목데이터 기반으로 미사용 상태이던 `components/projects/assignment-form-modal.tsx`를 실 API 연동 공용 컴포넌트로 교체, `assignments/page.tsx`의 인라인 등록 모달을 이 컴포넌트로 대체. `fixedPjtId`/`fixedPjtName` prop 신규 추가로 프로젝트 상세 화면에서는 프로젝트 선택 없이 고정 등록, 투입 관리 화면에서는 기존과 동일하게 프로젝트 선택 후 등록. `projects/[id]/page.tsx`가 이미 조회해둔 `employees` 배열을 반환값에 노출(신규 API 호출 없이 재사용). 백엔드 변경 없음, pytest 107개 그대로 통과, 실 서버 curl로 `POST /api/v1/assignments` 정상 등록(201) 확인(검증용 임시 프로젝트·사원은 삭제). §9-1 "프로젝트 상세 화면 인력투입 버튼" 항목 `[x]` 처리 — 프로젝트 섹션 §9-1 항목 전부 완료 | — |

