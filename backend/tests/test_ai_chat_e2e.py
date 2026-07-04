"""AI Chat 엔드투엔드 질의 검증 (로드맵 §8 "테스트 질의 10개 이상 검증", 직무 유형 포함).

`test_ai_parser.py`는 `parse_query` 단위 파싱만 검증하고, 이 파일은 실제 사용자가 겪는
전체 경로 — `POST /api/v1/ai/chat` → `parse_query` → (resource_search면) `availability.view`
권한 확인 → `search_resources` → 결정적 요약 응답 — 을 자연어 질의 10개 이상으로 검증한다.
직무 유형이 인식되는 질의가 실제로 LLM을 거치지 않고(`call_llm` 미호출) 결정적 요약을
반환하는지 확인하는 것이 핵심이다 — LLM이 호출되면 그 질의는 조건 인식에 실패해
`intent="unknown"`으로 새어나갔다는 뜻이므로 이 자체가 회귀 감지 역할을 한다.
"""

import pytest

import app.api.v1.ai_chat as ai_chat_module

# 사용자가 실제로 제시한 예시 질의 10개(§8 "자연어 조건 파싱 구현" 작업 당시 확정) —
# 전부 직무 유형/기술/부서/가동일 중 하나 이상이 인식되어 resource_search로 분류돼야 한다.
RESOURCE_SEARCH_QUERIES = [
    "다음 달 투입 가능한 Java 아키텍트 추천해줘",
    "8월에 가능한 Spring 개발자 찾아줘",
    "개발1팀에서 Python 가능한 사람 있어?",
    "이번 달 종료 예정자 알려줘",
    "가동률 50% 이하인 PM 찾아줘",
    "K-ICS 경험 있는 BA 찾아줘",
    "PostgreSQL 가능한 백엔드 개발자",
    "즉시 투입 가능한 시니어 개발자",
    "다음 주부터 가능한 React 개발자",
    "보험 프로젝트 경험 있는 아키텍트",
]


def _fail_if_llm_called(message):
    raise AssertionError(f"resource_search로 인식돼야 할 질의가 LLM으로 새어나갔다: {message!r}")


@pytest.mark.parametrize("message", RESOURCE_SEARCH_QUERIES)
def test_resource_search_query_never_reaches_llm(client, admin_token, monkeypatch, message):
    monkeypatch.setattr(ai_chat_module, "call_llm", _fail_if_llm_called)
    headers = {"Authorization": f"Bearer {admin_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": message})

    assert resp.status_code == 200
    reply = resp.json()["reply"]
    assert isinstance(reply, str) and reply
    # 권한 확인을 통과한 admin 계정이므로 권한 부족 안내 문구가 아니어야 한다.
    assert "권한이 없습니다" not in reply


def test_greeting_query_falls_back_to_llm(client, admin_token, monkeypatch):
    """직무 유형 등 조건이 전혀 없는 일반 대화는 그대로 LLM 경로를 타야 한다(회귀 확인)."""
    monkeypatch.setattr(ai_chat_module, "call_llm", lambda message: f"echo: {message}")
    headers = {"Authorization": f"Bearer {admin_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": "안녕하세요 반갑습니다"})

    assert resp.status_code == 200
    assert resp.json()["reply"] == "echo: 안녕하세요 반갑습니다"
