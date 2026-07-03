# HRM 자동화 시스템

SI/IT 조직 인력 현황·기술 스택·프로젝트 투입률·가동 가능일 통합 관리 시스템.
FastAPI + PostgreSQL + Next.js + Docker 기반. 상세 설계는 `plan_docs/[DESIGN]HRM_Automation_System_Design_v0_6.md`, 진행 상태는 `plan_docs/[BACKLOG]HRM_Automation_System_Roadmap.md` 참고.

## 기준 경로

`/App/hrmngr/`

## 포트

| 서비스 | 외부 포트 | 내부 포트 |
|---|---|---|
| Next.js (web) | 3030 | 3000 |
| FastAPI (api) | 8000 | 8000 |
| PostgreSQL (db) | 5442 | 5432 |
| Redis | - (내부 전용) | 6379 |

## 최초 기동

```bash
cp .env.example .env
# .env 값 수정 (DB 비밀번호, JWT_SECRET_KEY, 서버 IP 등)

docker compose up -d --build
```

확인:

```bash
curl http://localhost:8000/health          # FastAPI 헬스체크
curl -I http://localhost:3030              # Next.js
psql -h localhost -p 5442 -U hrm_user -d hrm   # PostgreSQL 접속
```

## 컨테이너 재기동

```bash
docker compose restart
# 또는 전체 재빌드
docker compose up -d --build
```

## DB 마이그레이션 (Alembic)

```bash
cd backend
alembic revision --autogenerate -m "설명"   # app/models/에 등록된 모델 기준 마이그레이션 생성
alembic upgrade head                          # 최신 마이그레이션까지 적용
alembic downgrade -1                          # 직전 마이그레이션으로 롤백
```

`DATABASE_URL`은 `.env`에서 로드된다 (`alembic.ini`에는 하드코딩하지 않음). 컨테이너 안에서 실행하려면 `docker compose exec api alembic upgrade head` 형태로 실행한다.

## DB 백업

```bash
bash backup/backup_db.sh
```

crontab 등록 (매일 02:00):

```
0 2 * * * /bin/bash /App/hrmngr/backup/backup_db.sh >> /App/hrmngr/logs/backup.log 2>&1
```
