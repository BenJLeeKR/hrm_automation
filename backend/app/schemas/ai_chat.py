from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """AI Chat 질의 요청 스키마 (`POST /api/v1/ai/chat`, SCR-012)"""

    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """AI Chat 응답 스키마 — 1차 구현 범위는 LLM 응답 텍스트만 반환한다."""

    reply: str
