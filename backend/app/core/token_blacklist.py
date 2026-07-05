import logging
from datetime import datetime, timezone

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

_KEY_PREFIX = "token_blacklist:"
_client: redis.Redis | None = None


def _get_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _client


def blacklist_token(jti: str, expires_at: datetime) -> None:
    """로그아웃(§9-1 "로그아웃 시 서버 측 즉시 토큰 무효화 미구현" 해소) 시 토큰을
    무효화한다 — 토큰 만료 시각까지만 Redis에 보관하고 그 이후에는 자동 만료(TTL)되어
    블랙리스트가 무한히 누적되지 않는다. Redis 연결 실패는 로그아웃 자체를 막지 않도록
    조용히 무시한다(클라이언트는 이미 로컬 토큰을 삭제하므로 사용자 경험에는 영향 없음 —
    `services/teams_notify.py`의 "선택적 연동 실패는 조용히 넘어간다" 원칙과 동일)."""
    ttl_seconds = int((expires_at - datetime.now(timezone.utc)).total_seconds())
    if ttl_seconds <= 0:
        return
    try:
        _get_client().set(f"{_KEY_PREFIX}{jti}", "1", ex=ttl_seconds)
    except redis.RedisError:
        logger.warning("토큰 블랙리스트 등록 실패 — Redis 연결 불가", exc_info=True)


def is_blacklisted(jti: str) -> bool:
    """토큰이 로그아웃 등으로 무효화되었는지 확인한다. Redis 장애 시에는 안전하게
    "무효화되지 않음"으로 판단(fail-open)한다 — 인증 자체는 JWT 서명·만료로 이미
    보장되므로, Redis 장애가 전체 로그인 불가로 번지지 않도록 한다."""
    try:
        return bool(_get_client().exists(f"{_KEY_PREFIX}{jti}"))
    except redis.RedisError:
        logger.warning("토큰 블랙리스트 조회 실패 — Redis 연결 불가, 무효화되지 않은 것으로 처리", exc_info=True)
        return False
