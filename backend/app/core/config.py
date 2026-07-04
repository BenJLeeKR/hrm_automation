from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "production"
    APP_NAME: str = "HRM Automation System"
    LOG_LEVEL: str = "INFO"

    POSTGRES_DB: str = "hrm"
    POSTGRES_USER: str = "hrm_user"
    POSTGRES_PASSWORD: str = ""
    DATABASE_URL: str = ""

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: str = "http://localhost:3030"
    REDIS_URL: str = "redis://hrm-redis:6379/0"

    # AI Chat(Phase 6, 로드맵 §8 "AI Chat 화면 구현") — LLM_PROVIDER로 사용할 공급자를
    # 선택하는 간단한 추상화. 현재는 DeepSeek(OpenAI 호환 API)만 지원하며, 향후 다른
    # 공급자를 추가할 때 이 필드 기준으로 분기한다(`app/services/ai_chat.py` 참조).
    LLM_PROVIDER: str = "deepseek"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL_ID: str = "deepseek-chat"
    OPENAI_API_KEY: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
