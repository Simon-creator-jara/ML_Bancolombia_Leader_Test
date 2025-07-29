import pytest
from pydantic import ValidationError
from src.domain.model.health.health_model import HealthResponse


def test_health_model():
    """Test valid initialization of the HealthResponse model with correct
    types."""
    health_response = HealthResponse(
        check_state=True, message="OK", date="2021-01-01T00:00:00"
    )
    assert health_response.check_state is True
    assert health_response.message == "OK"
    assert health_response.date == "2021-01-01T00:00:00"


def test_health_model_error():
    """Test that HealthResponse raises ValidationError when given invalid
    types."""
    with pytest.raises(ValidationError):
        HealthResponse(check_state="test", message="OK",
                       date="2021-01-01T00:00:00")
