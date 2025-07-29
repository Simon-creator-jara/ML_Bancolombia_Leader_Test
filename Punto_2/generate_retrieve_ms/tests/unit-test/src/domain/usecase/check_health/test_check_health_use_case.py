from datetime import datetime

import pytest

from src.domain.model.health.health_model import HealthResponse
from src.domain.usecase.check_health.check_health_use_case import \
    CheckHealthUseCase


@pytest.mark.asyncio
async def test_check_health_use_case():
    """Test that the health check use case returns valid health status
    information.

    Verifies that CheckHealthUseCase correctly:
    - Returns a properly formed HealthResponse object
    - Sets check_state to True to indicate the service is running
    - Sets message to "ALIVE"
    - Includes a valid ISO format date string
    """
    config = {"key": "value"}
    logger = "logger"
    check_health_use_case = CheckHealthUseCase(config, logger)
    health_response = await check_health_use_case.check()
    assert isinstance(health_response, HealthResponse)
    assert health_response.check_state
    assert health_response.message == "ALIVE"
    datetime.fromisoformat(health_response.date)
