import pytest
from pydantic import ValidationError
from src.domain.model.answer.answer_model import answer, GenerateAnswerRequest

def test_answer_model_valid():
    q = answer(answer=[1,2,4])
    assert q.answer == [1,2,4]

def test_answer_model_missing_field():
    with pytest.raises(ValidationError) as excinfo:
        answer()


def test_answer_model_invalid_type():
    with pytest.raises(ValidationError) as excinfo:
        answer(answer=123)

def test_generate_answer_request_valid():
    q = GenerateAnswerRequest(question="What is the capital of France?", answer=[1, 2, 3])
    assert q.question == "What is the capital of France?"
    assert q.answer == [1, 2, 3]

def test_generate_answer_request_missing_field():
    with pytest.raises(ValidationError) as excinfo:
        GenerateAnswerRequest(question="What is the capital of France?")
    assert "answer" in str(excinfo.value)