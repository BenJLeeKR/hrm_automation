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

    # 운영 자동화 배치(Phase 7, 로드맵 §8 "PJT_ASGN_END_ALERT 배치 구현") — Teams Incoming
    # Webhook URL. 미설정 시(로컬/개발 환경) 알림 전송을 건너뛰고 배치 자체는 정상 실행한다
    # (`app/services/teams_notify.py` 참조) — DEEPSEEK_API_KEY와 동일한 선택적 연동 패턴.
    TEAMS_WEBHOOK_URL: str = ""

    # 알림 채널(SYS_CONFIG) DB 값이 NULL일 때 폴백으로 쓰는 SMTP 환경변수 (설계서 §5.3.17
    # "폴백 정책"). `.env.example`에 이미 자리만 잡혀 있던 값들을 실제로 읽어 쓴다.
    SMTP_HOST: str = ""
    SMTP_PORT: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""

    # SYS_CONFIG.IS_SECRET=TRUE 값(SMTP 비밀번호 등) 암호화 키 (설계서 §5.3.17, 2026-07-05
    # "일반 설정" §9-1 리스크 해소). 32바이트를 base64 인코딩한 값 — `Fernet.generate_key()`로
    # 생성. 미설정 시 알림 채널 설정 저장/조회 API가 500으로 실패한다(app/core/crypto.py).
    CONFIG_ENCRYPTION_KEY: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
