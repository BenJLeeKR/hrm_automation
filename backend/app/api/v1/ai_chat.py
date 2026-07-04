from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import has_permission, require_permission
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.schemas.ai_chat import ChatRequest, ChatResponse
from app.services.ai_chat import LlmCallError, call_llm
from app.services.ai_parser import parse_query
from app.services.ai_resource_search import search_resources

router = APIRouter(prefix="/ai", tags=["ai-chat"])

# resource_search 응답은 사실상 "가동 가능 인력"(SCR-010, `availability` 화면) 데이터를
# 그대로 노출하므로, `ai_chat.view`(전 역할 허용)와 별도로 `availability.view` 권한을
# 추가로 확인한다 — 그렇지 않으면 화면 설계서상 SCR-010 접근이 제외된 역할(VIEWER)이
# AI Chat을 우회 경로 삼아 동일한 정보를 열람할 수 있다(로드맵 §9 리스크).
_RESOURCE_SEARCH_SCREEN = "availability"
_NO_PERMISSION_REPLY = "가동 인력 상세 조회 권한이 없습니다. 필요한 경우 관리자에게 권한을 요청하세요."


@router.post("/chat", response_model=ChatResponse)
def post_ai_chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("ai_chat", "view")),
) -> ChatResponse:
    """AI Chat 질의 (SCR-012 — 로드맵 §8 "권한 필터링 후 LLM 컨텍스트 전달 구현").

    메시지를 `parse_query`(규칙 기반, LLM 미사용)로 먼저 파싱해 `intent`가
    `resource_search`로 인식되면(직무 유형/기술/부서/가동일 중 하나라도 매칭) 기존
    `list_availability` repository로 whitelist 조회만 수행하고, 그 결정적(deterministic)
    결과 요약을 그대로 응답한다 — 이 경로는 LLM을 거치지 않아 환각 위험이 없다.
    그 외(intent="unknown")에는 기존 1차 구현 범위(LLM 단순 호출/응답)를 그대로 유지한다.

    `resource_search` 응답을 반환하기 전에 요청자의 `PERM_JSON`에 `availability.view`
    권한이 있는지 확인한다 — 없으면 조회를 실행하지 않고 안내 메시지만 반환한다(SCR-010
    화면 설계서 접근 권한과 동일 기준 적용). 부서 단위 등 행(row) 단위 세부 범위 제한은
    `app/api/deps.py`의 `require_permission` 기존 한계와 동일하게 이번 범위에서 다루지
    않는다. 환각 방지 프롬프트는 §9 리스크에 후속 작업으로 남겨뒀다.
    """
    parsed = parse_query(db, payload.message)

    if parsed.intent == "resource_search":
        if not has_permission(db, current_user, _RESOURCE_SEARCH_SCREEN, "view"):
            return ChatResponse(reply=_NO_PERMISSION_REPLY)
        result = search_resources(db, parsed)
        return ChatResponse(reply=result.summary)

    try:
        reply = call_llm(payload.message)
    except LlmCallError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from None

    return ChatResponse(reply=reply)
