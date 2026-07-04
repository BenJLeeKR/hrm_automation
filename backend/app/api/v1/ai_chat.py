from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import require_permission
from app.schemas.ai_chat import ChatRequest, ChatResponse
from app.services.ai_chat import LlmCallError, call_llm

router = APIRouter(prefix="/ai", tags=["ai-chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[Depends(require_permission("ai_chat", "view"))],
)
def post_ai_chat(payload: ChatRequest) -> ChatResponse:
    """AI Chat 질의 (SCR-012 — 로드맵 §8 "AI Chat 화면 구현").

    1차 구현 범위는 LLM 단순 호출/응답만 다룬다 — 자연어 조건 파싱·DB 조회 연동은
    후속 작업으로 분리했다(`app/services/ai_chat.py` 주석, 로드맵 §9 참조).
    """
    try:
        reply = call_llm(payload.message)
    except LlmCallError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from None

    return ChatResponse(reply=reply)
