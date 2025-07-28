from unittest.mock import AsyncMock

import pytest

from src.domain.model.health.health_model import HealthResponse
from src.infraestructure.entry_points.fast_api.handlers.health_handler import \
    HealthHandler


@pytest.mark.asyncio
async def test_health_handler_check_success():
    """Test successful health check through the handler.

    Verifies that the health handler correctly:
    - Calls the health check use case
    - Returns the expected health response object
    """
    mock_usecase = AsyncMock()
    expected_response = HealthResponse(
        check_state=True,
        message="Service is healthy",
        date="2025-04-25"
    )
    mock_usecase.check.return_value = expected_response
    handler = HealthHandler(usecase=mock_usecase)

    response = await handler.check()

    assert response == expected_response
    mock_usecase.check.assert_called_once()


@pytest.mark.asyncio
async def test_health_handler_check_failure():
    """Test error handling when health check fails.

    Verifies that the health handler correctly:
    - Propagates exceptions from the use case
    - Preserves the original error message
    """
    mock_usecase = AsyncMock()
    mock_usecase.check.side_effect = Exception("Unexpected Error")
    handler = HealthHandler(usecase=mock_usecase)

    with pytest.raises(Exception) as exc_info:
        await handler.check()

    assert str(exc_info.value) == "Unexpected Error"
    mock_usecase.check.assert_called_once()
