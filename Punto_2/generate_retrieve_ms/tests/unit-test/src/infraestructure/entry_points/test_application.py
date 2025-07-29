from unittest.mock import MagicMock, patch
import pytest

from fastapi import FastAPI, APIRouter

from src.infraestructure.entry_points.application import (
    create_application, include_router
)


class TestApplication:
    """Test suite for the FastAPI application creation and router
    configuration."""
    @pytest.fixture
    def mock_container(self):
        """Create a mock dependency container.

        Returns:
            MagicMock: A configured mock container with url_prefix set to
            "/api/v1".
        """
        container = MagicMock()
        container.app_config.url_prefix = "/api/v1"
        return container

    @pytest.fixture
    def mock_router(self):
        """Create a mock FastAPI router.

        Returns:
            MagicMock: A mock object with APIRouter specification.
        """
        return MagicMock(spec=APIRouter)

    def test_include_router(self, mock_router):
        """Test that routes are correctly included in the FastAPI application.

        Verifies that the include_router function:
        - Calls set_routes with the correct prefix
        - Includes the router in the FastAPI application

        Args:
            mock_router: A mock router fixture.
        """
        mock_app = MagicMock(spec=FastAPI)
        with patch("src.infraestructure.entry_points.application.set_routes",
                   return_value=mock_router) as mock_set_routes:
            include_router(mock_app, prefix="/test-prefix")
            mock_set_routes.assert_called_once_with("/test-prefix")
            mock_app.include_router.assert_called_once_with(mock_router)

    def test_create_application(self, mock_container, mock_router):
        """Test the complete application creation process.

        Verifies that the create_application function:
        - Gets the dependency container
        - Creates a FastAPI instance
        - Assigns the container to the app
        - Sets up routes with the correct prefix
        - Includes the router in the app
        - Returns the configured FastAPI instance

        Args:
            mock_container: A mock dependency container fixture.
            mock_router: A mock router fixture.
        """
        # Mock the dependencies
        with patch(
            "src.infraestructure.entry_points.application.get_deps_container",
            return_value=mock_container
        ) as mock_get_container, \
                patch(
                    "src.infraestructure.entry_points.application.set_routes",
                    return_value=mock_router
                ) as mock_set_routes, \
                patch(
                    "src.infraestructure.entry_points.application.FastAPI"
                ) as mock_fastapi_class:
            # Setup the mock FastAPI instance
            mock_app = MagicMock(spec=FastAPI)
            mock_fastapi_class.return_value = mock_app
            result = create_application()
            mock_get_container.assert_called_once()
            mock_fastapi_class.assert_called_once()
            assert mock_app.container == mock_container
            mock_set_routes.assert_called_once_with("/api/v1")
            mock_app.include_router.assert_called_once_with(mock_router)
            assert result == mock_app

    def test_create_application_integration(self):
        """Test integration of the application creation components.

        Verifies that create_application:
        - Returns an actual FastAPI instance (not a mock)
        - Attaches the container to the application
        - Calls include_router with the correct prefix

        This test integrates more real components compared to
        test_create_application which uses more mocks.
        """
        mock_container = MagicMock()
        mock_container.app_config.url_prefix = "/api/v1"
        with patch(
            "src.infraestructure.entry_points.application.get_deps_container",
            return_value=mock_container
        ), \
                patch(
                    "src.infraestructure.entry_points.application."
                    "include_router"
                ) as mock_include_router:
            app = create_application()
            assert isinstance(app, FastAPI)
            assert app.container == mock_container
            mock_include_router.assert_called_once_with(app, prefix="/api/v1")
