from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.db.base import Base

# Phase 2에서 테이블별 ORM 모델이 추가되면 app/models/__init__.py에서 해당 모델을
# import해야 한다 (모델이 import되어야 Base.metadata에 등록되고 autogenerate 대상이 됨).
import app.models  # noqa: E402,F401

# Alembic Config object — alembic.ini의 값에 접근하기 위한 객체
config = context.config

# .ini에는 sqlalchemy.url을 비워두고, 여기서 .env 기반 DATABASE_URL로 덮어쓴다
# (비밀번호 등 민감정보를 alembic.ini에 하드코딩하지 않기 위함)
# alembic.ini는 내부적으로 ConfigParser(BasicInterpolation)를 사용해 "%"를 보간 문법으로
# 해석하므로, percent-encoding된 비밀번호(예: %40)가 URL에 포함되면 set_main_option에서
# "invalid interpolation syntax" 오류가 난다. "%"를 "%%"로 이스케이프해 저장하면
# get_main_option/engine_from_config에서 조회할 때 다시 "%"로 정상 복원된다 (Alembic 공식
# 권장 우회 방법).
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """--sql 옵션 등으로 DB 연결 없이 마이그레이션 스크립트만 생성할 때 사용."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """실제 DB에 연결해 마이그레이션을 적용할 때 사용 (`alembic upgrade head` 등)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
