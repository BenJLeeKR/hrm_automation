"""`app/services/ai_chat.py`의 `call_llm` 자체를 검증 — 실제 네트워크 호출 없이
`httpx.post`를 모킹해 요청 페이로드(환각 방지 시스템 프롬프트 포함 여부)를 확인한다."""

import app.services.ai_chat as ai_chat_service
from app.core.config import settings


class _FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"choices": [{"message": {"content": "ok"}}]}


def test_call_llm_includes_anti_hallucination_system_prompt(monkeypatch):
    monkeypatch.setattr(settings, "DEEPSEEK_API_KEY", "test-key")
    captured = {}

    def _fake_post(url, headers, json, timeout):
        captured["json"] = json
        return _FakeResponse()

    monkeypatch.setattr(ai_chat_service.httpx, "post", _fake_post)

    reply = ai_chat_service.call_llm("안녕")

    assert reply == "ok"
    messages = captured["json"]["messages"]
    assert messages[0]["role"] == "system"
    assert "지어내" in messages[0]["content"]
    assert messages[1] == {"role": "user", "content": "안녕"}
