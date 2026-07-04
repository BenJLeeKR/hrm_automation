import httpx

from app.core.config import settings

# AI Chat 1차 구현 범위(로드맵 §8 "AI Chat 화면 구현", 사용자 확정 — §9 리스크 참조):
# LLM 단순 호출/응답만 다룬다. 자연어 조건 파싱 → SQL 조회 → 결과 요약 흐름, 권한 필터링
# 기반 컨텍스트 전달은 이후 §8 작업에서 완료했다(`app/services/ai_parser.py`,
# `app/services/ai_resource_search.py`, `app/api/v1/ai_chat.py`의 `availability.view`
# 확인 로직 참조). 이 모듈(`call_llm`)은 그중에서도 `intent="unknown"`(리소스 검색으로
# 인식되지 않은 자유 대화)일 때만 호출되는 경로다 — resource_search 경로는 LLM을 거치지
# 않는 결정적 요약이라 이 모듈과 무관하게 이미 환각 위험이 없다.

_REQUEST_TIMEOUT_SECONDS = 30.0

# 환각 방지 시스템 프롬프트(로드맵 §8 "환각 방지 시스템 프롬프트 적용") — 이 경로는 DB를
# 조회하지 않는 자유 대화 호출이므로, LLM이 실제로 조회하지 않은 사원명·프로젝트명·투입률·
# 날짜 등 구체적인 HR 데이터를 지어내지 않도록 명시적으로 금지하고, 그런 질의는 시스템
# 내장 검색으로 유도한다.
_ANTI_HALLUCINATION_SYSTEM_PROMPT = (
    "당신은 HRM(인력 관리) 시스템의 AI 어시스턴트입니다. "
    "이 대화에는 실제 데이터베이스 조회 결과가 포함되어 있지 않습니다. "
    "따라서 실존 여부를 확인할 수 없는 사원 이름, 사번, 프로젝트명, 투입률(%), 가동일, "
    "조직/부서 배치 등 구체적인 인력관리 데이터를 절대로 지어내거나 추측해서 답하지 마세요. "
    "사용자가 특정 인력 검색·추천·가동 현황을 물으면, 답을 지어내는 대신 "
    "\"해당 조회는 정확한 결과를 위해 직무 유형·기술·가동 가능일 등 조건을 포함해 다시 "
    "질문해 주세요\"처럼 시스템의 조회 기능을 이용하도록 안내하세요. "
    "확실하지 않은 내용은 모른다고 명확히 밝히고, 일반적인 안내나 인사말에는 자연스럽게 응답하세요."
)


class LlmCallError(Exception):
    """LLM 공급자 호출 실패(네트워크 오류, 인증 실패, 타임아웃 등)를 감싸는 예외."""


def call_llm(message: str) -> str:
    """사용자 메시지를 LLM에 전달하고 응답 텍스트를 반환한다.

    `LLM_PROVIDER`로 공급자를 선택하는 간단한 추상화 — 현재는 DeepSeek(OpenAI 호환
    `chat/completions` API)만 지원한다. 향후 다른 공급자를 추가할 때는 이 분기만
    확장하면 된다. 매 호출마다 `_ANTI_HALLUCINATION_SYSTEM_PROMPT`를 시스템 메시지로
    함께 전달해, DB 조회 없이 답하는 이 경로에서 LLM이 실존 여부를 알 수 없는 사원/
    프로젝트 정보를 지어내지 않도록 한다.
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
                "messages": [
                    {"role": "system", "content": _ANTI_HALLUCINATION_SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
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
