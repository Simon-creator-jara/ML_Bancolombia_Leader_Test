import pytest
from pydantic import ValidationError
from src.domain.model.message_error.message_error_model import MessageError


def test_message_error_model():
    """Test valid initialization of the MessageError model with correct
    types."""
    message_error = MessageError(subject_message="Test subject",
                                 content_message="Test content")
    assert message_error.subject_message == "Test subject"
    assert message_error.content_message == "Test content"


def test_message_error_model_error():
    """Test that MessageError raises ValidationError when given invalid
    types."""
    with pytest.raises(ValidationError):
        MessageError(subject_message=123,
                     content_message="Test content")
