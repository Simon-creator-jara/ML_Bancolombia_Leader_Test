import pytest
import asyncio
from unittest.mock import MagicMock
from src.infraestructure.driven_adapters.openai.adapter.openai_adapter import OpenAIQuestionImprover

class DummyChoice:
    def __init__(self, content):
        self.message = type("M", (), {"content": content})

class DummyResponse:
    def __init__(self, content):
        self.choices = [DummyChoice(content)]

@pytest.mark.asyncio
async def test_improve_returns_improved_question(monkeypatch):
    mock_client = MagicMock()
    mock_create = MagicMock(return_value=DummyResponse("Improved?"))
    mock_client.chat = MagicMock(completions=MagicMock(create=mock_create))
    async def fake_to_thread(func, *args, **kwargs):
        return func(*args, **kwargs)
    monkeypatch.setattr(asyncio, "to_thread", fake_to_thread)

    improver = OpenAIQuestionImprover(mock_client)
    result = await improver.improve("Original?")

    assert result == "Improved?"
    expected_prompt = (
        "You are a helpful assistant…\n\n"
        'Original question: "Original?"\n\n'
        "Improved version:"
    )
    mock_create.assert_called_once_with(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You improve questions for retrieval."},
            {"role": "user",   "content": expected_prompt},
        ],
        temperature=0,
        max_tokens=512
    )
