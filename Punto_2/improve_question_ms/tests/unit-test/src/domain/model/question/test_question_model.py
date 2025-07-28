import pytest
from pydantic import ValidationError
from src.domain.model.question.question_model import question

def test_question_model_valid():
    q = question(question="What is your name?")
    assert q.question == "What is your name?"

def test_question_model_missing_field():
    with pytest.raises(ValidationError) as excinfo:
        question()


def test_question_model_invalid_type():
    with pytest.raises(ValidationError) as excinfo:
        question(question=123)
