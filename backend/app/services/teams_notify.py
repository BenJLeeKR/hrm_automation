import httpx

from app.core.config import settings

_REQUEST_TIMEOUT_SECONDS = 10.0


class TeamsNotifyError(Exception):
    """Teams Webhook 전송 실패(네트워크 오류, 인증 실패 등)를 감싸는 예외."""


def send_teams_message(text: str) -> bool:
    """`TEAMS_WEBHOOK_URL`이 설정되어 있으면 Teams Incoming Webhook으로 메시지를 보내고
    `True`를 반환한다. 미설정 시(로컬/개발 환경 등)에는 조용히 건너뛰고 `False`를
    반환한다 — 배치 자체는 알림 채널 유무와 무관하게 정상 실행되어야 하므로, AI Chat의
    `DEEPSEEK_API_KEY` 미설정 시 처리(`app/services/ai_chat.py`)와 달리 예외를 던지지
    않는다. 전송을 시도했지만 실패한 경우(URL은 있으나 요청이 실패)만 예외를 던진다.
    """
    if not settings.TEAMS_WEBHOOK_URL:
        return False

    try:
        response = httpx.post(
            settings.TEAMS_WEBHOOK_URL,
            json={"text": text},
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise TeamsNotifyError(f"Teams 알림 전송이 실패했습니다: {exc}") from exc

    return True
