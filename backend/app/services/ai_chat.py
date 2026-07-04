import httpx

from app.core.config import settings

# AI Chat 1차 구현 범위(로드맵 §8 "AI Chat 화면 구현", 사용자 확정 — §9 리스크 참조):
# LLM 단순 호출/응답만 다룬다. 자연어 조건 파싱 → SQL 조회 → 결과 요약 흐름, 권한 필터링
# 기반 컨텍스트 전달, 환각 방지 프롬프트, 테스트 질의 검증은 Phase 6 후속 작업으로 분리했다
# (`[DESIGN]HRM_Screen_Design.md` SCR-012 전체 파이프라인 중 LLM 호출 구간만 구현).

_REQUEST_TIMEOUT_SECONDS = 30.0


class LlmCallError(Exception):
    """LLM 공급자 호출 실패(네트워크 오류, 인증 실패, 타임아웃 등)를 감싸는 예외."""


def call_llm(message: str) -> str:
    """사용자 메시지를 LLM에 전달하고 응답 텍스트를 반환한다.

    `LLM_PROVIDER`로 공급자를 선택하는 간단한 추상화 — 현재는 DeepSeek(OpenAI 호환
    `chat/completions` API)만 지원한다. 향후 다른 공급자를 추가할 때는 이 분기만
    확장하면 된다.
    """
    if settings.LLM_PROVIDER != "deepseek":
        raise LlmCallError(f"지원하지 않는 LLM_PROVIDER입니다: {settings.LLM_PROVIDER}")
    if not settings.DEEPSEEK_API_KEY:
        raise LlmCallError("DEEPSEEK_API_KEY가 설정되어 있지 않습니다.")

    try:
        response = httpx.post(
            f"{settings.DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.DEEPSEEK_MODEL_ID,
                "messages": [{"role": "user", "content": message}],
            },
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise LlmCallError(f"LLM 호출이 실패했습니다 (HTTP {exc.response.status_code}).") from exc
    except httpx.HTTPError as exc:
        raise LlmCallError("LLM 서버에 연결할 수 없습니다. 잠시 후 다시 시도하세요.") from exc

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise LlmCallError("LLM 응답 형식이 올바르지 않습니다.") from exc
