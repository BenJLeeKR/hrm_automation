import uuid
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


class ResourceSearchItem(BaseModel):
    """리소스 검색 결과 1건 — `GET /api/v1/availability`(`list_availability`) 계산 결과에
    사원 이름/사번을 조인한 요약용 스키마."""

    EMPL_ID: uuid.UUID
    EMPL_NO: str
    EMPL_NM: str
    AVAIL_STAT_CD: str
    AVAIL_RT: int
    AVAIL_STRT_DT: date | None


class ResourceSearchResult(BaseModel):
    """`ParsedResourceQuery`(`intent="resource_search"`)를 whitelist 기반으로 실행한
    검색 결과 — `backend/app/services/ai_resource_search.py`의 `search_resources`가 반환한다."""

    total: int
    items: list[ResourceSearchItem]
    summary: str
    skipped_skills: list[str] = Field(default_factory=list)
