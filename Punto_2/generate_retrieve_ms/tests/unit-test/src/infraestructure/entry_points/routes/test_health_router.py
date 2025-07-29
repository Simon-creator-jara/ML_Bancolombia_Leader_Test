from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.infraestructure.entry_points.routes.health_router import (
    get_health_usecase, router)


@pytest.fixture
def mock_container():
    """Create a mock container with health use case."""
    container = MagicMock()
    container.check_health_use_case = AsyncMock()
    return container


@pytest.fixture
def app(mock_container):
    """Create a FastAPI app with the health router."""
    app = FastAPI()
    app.container = mock_container
    app.include_router(router, prefix="/health")
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_health_usecase(mock_container):
    """Test the get_health_usecase dependency."""
    mock_request = MagicMock(spec=Request)
    mock_request.app.container = mock_container
    result = await get_health_usecase(mock_request)
    assert result == mock_container.check_health_use_case


def test_health_check_route(client, mock_container):
    """Test the health check route."""
    mock_health_result = {"status": "ok", "version": "1.0.0"}
    mock_container.check_health_use_case.return_value = mock_health_result
    with patch(
        "src.infraestructure.entry_points.routes.health_router.HealthHandler"
    ) as mock_handler_class:
        mock_handler = AsyncMock()
        mock_handler.check.return_value = mock_health_result
        mock_handler_class.return_value = mock_handler
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == mock_health_result
        mock_handler_class.assert_called_once_with(
            mock_container.check_health_use_case
        )
        mock_handler.check.assert_called_once()
