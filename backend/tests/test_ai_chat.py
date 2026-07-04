"""AI Chat 테스트 — 실제 LLM 네트워크 호출은 하지 않고 `call_llm`을 모킹한다
(반복 실행 가능성·오프라인 실행을 위해, 실제 DeepSeek 연동 자체는 수동 curl로 검증 완료)."""

import app.api.v1.ai_chat as ai_chat_module
from app.services.ai_chat import LlmCallError


def test_chat_returns_llm_reply(client, admin_token, monkeypatch):
    monkeypatch.setattr(ai_chat_module, "call_llm", lambda message: f"echo: {message}")
    headers = {"Authorization": f"Bearer {admin_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": "안녕"})

    assert resp.status_code == 200
    assert resp.json() == {"reply": "echo: 안녕"}


def test_chat_requires_auth(client):
    resp = client.post("/api/v1/ai/chat", json={"message": "안녕"})

    assert resp.status_code == 401


def test_chat_rejects_empty_message(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": ""})

    assert resp.status_code == 422


def test_chat_llm_failure_returns_502(client, admin_token, monkeypatch):
    def _raise(message):
        raise LlmCallError("LLM 서버에 연결할 수 없습니다.")

    monkeypatch.setattr(ai_chat_module, "call_llm", _raise)
    headers = {"Authorization": f"Bearer {admin_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": "안녕"})

    assert resp.status_code == 502


def test_viewer_can_use_ai_chat(client, viewer_token, monkeypatch):
    """설계서(SCR-012) 접근 권한이 A H P T E V로 전 역할 허용이므로 VIEWER도 가능해야 한다."""
    monkeypatch.setattr(ai_chat_module, "call_llm", lambda message: "ok")
    headers = {"Authorization": f"Bearer {viewer_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": "안녕"})

    assert resp.status_code == 200


def test_chat_resource_search_intent_bypasses_llm(client, admin_token, monkeypatch):
    """직무 유형 등 조건이 인식되면(resource_search) LLM을 호출하지 않고 결정적 요약을 반환해야 한다."""

    def _fail_if_called(message):
        raise AssertionError("resource_search intent에서는 call_llm이 호출되면 안 된다")

    monkeypatch.setattr(ai_chat_module, "call_llm", _fail_if_called)
    headers = {"Authorization": f"Bearer {admin_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": "즉시 투입 가능한 PM 찾아줘"})

    assert resp.status_code == 200
    assert "찾" in resp.json()["reply"]


def test_chat_resource_search_denied_for_role_without_availability_view(client, viewer_token, monkeypatch):
    """VIEWER는 SCR-010(가동 가능 인력) 접근 권한이 없으므로, AI Chat을 통한 우회 조회도
    차단하고 안내 메시지만 반환해야 한다(로드맵 §9 리스크 — 권한 필터링)."""

    def _fail_if_called(message):
        raise AssertionError("권한이 없는 resource_search에서는 call_llm도 호출되면 안 된다")

    monkeypatch.setattr(ai_chat_module, "call_llm", _fail_if_called)
    headers = {"Authorization": f"Bearer {viewer_token}"}

    resp = client.post("/api/v1/ai/chat", headers=headers, json={"message": "즉시 투입 가능한 PM 찾아줘"})

    assert resp.status_code == 200
    assert resp.json()["reply"] == "가동 인력 상세 조회 권한이 없습니다. 필요한 경우 관리자에게 권한을 요청하세요."
