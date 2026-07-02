#!/bin/bash
set -euo pipefail

BACKUP_DIR="/App/hrmngr/backup/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

docker compose -f /App/hrmngr/docker-compose.yml exec -T db \
  pg_dump -U hrm_user -d hrm | gzip > "${BACKUP_DIR}/hrm_${TIMESTAMP}.sql.gz"

find "${BACKUP_DIR}" -name "*.sql.gz" -mtime +14 -delete
