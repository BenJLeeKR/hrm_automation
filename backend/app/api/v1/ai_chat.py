from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.db.session import get_db
from app.schemas.ai_chat import ChatRequest, ChatResponse
from app.services.ai_chat import LlmCallError, call_llm
from app.services.ai_parser import parse_query
from app.services.ai_resource_search import search_resources

router = APIRouter(prefix="/ai", tags=["ai-chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[Depends(require_permission("ai_chat", "view"))],
)
def post_ai_chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """AI Chat 질의 (SCR-012 — 로드맵 §8 "파싱 결과 → SQL 조회 → 결과 요약 흐름 구현").

    메시지를 `parse_query`(규칙 기반, LLM 미사용)로 먼저 파싱해 `intent`가
    `resource_search`로 인식되면(직무 유형/기술/부서/가동일 중 하나라도 매칭) 기존
    `list_availability` repository로 whitelist 조회만 수행하고, 그 결정적(deterministic)
    결과 요약을 그대로 응답한다 — 이 경로는 LLM을 거치지 않아 환각 위험이 없다.
    그 외(intent="unknown")에는 기존 1차 구현 범위(LLM 단순 호출/응답)를 그대로 유지한다.

    권한 필터링(조회 결과를 요청자 권한 범위로 제한)과 환각 방지 프롬프트는 아직 적용하지
    않는다 — 로드맵 §9 리스크 및 §4 Phase 6 표에 후속 작업으로 남겨뒀다.
    """
    parsed = parse_query(db, payload.message)

    if parsed.intent == "resource_search":
        result = search_resources(db, parsed)
        return ChatResponse(reply=result.summary)

    try:
        reply = call_llm(payload.message)
    except LlmCallError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from None

    return ChatResponse(reply=reply)
