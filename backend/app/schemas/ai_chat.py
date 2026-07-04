from datetime import date

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """AI Chat 질의 요청 스키마 (`POST /api/v1/ai/chat`, SCR-012)"""

    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """AI Chat 응답 스키마 — 1차 구현 범위는 LLM 응답 텍스트만 반환한다."""

    reply: str


class ParsedResourceQuery(BaseModel):
    """자연어 조건 파싱 결과 표준 스키마 (로드맵 §8 "자연어 조건 파싱 구현").

    `backend/app/services/ai_parser.py`의 `parse_query`가 반환하는 내부 표준 형태다.
    이번 작업 범위는 파싱까지만이며, 이 결과를 실제 SQL 조회(리소스 검색 API 호출)에
    연결하는 것은 후속 작업("파싱 결과 → SQL 조회 → 결과 요약 흐름 구현")에서 다룬다.
    """

    intent: str
    job_type: str | None = None
    skills: list[str] = Field(default_factory=list)
    min_proficiency_level: int | None = None
    available_from: date | None = None
    department: str | None = None
    confidence: float
    unresolved_terms: list[str] = Field(default_factory=list)
