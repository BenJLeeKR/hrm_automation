from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """모든 SQLAlchemy ORM 모델의 공통 베이스. Alembic env.py의 target_metadata가 이 클래스의
    metadata를 참조하므로, Phase 2에서 추가되는 모델은 반드시 이 Base를 상속해야 마이그레이션
    autogenerate 대상에 포함된다."""
