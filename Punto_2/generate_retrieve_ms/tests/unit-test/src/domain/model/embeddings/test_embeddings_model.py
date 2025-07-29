import pytest
from pydantic import ValidationError
from src.domain.model.embeddings.embeddings_model import question


def test_question_accepts_valid_question():
    ds = question(question="Soy una prueba?")
    assert ds.question == "Soy una prueba?"


def test_question_requires_question():
    with pytest.raises(ValidationError):
        question()
