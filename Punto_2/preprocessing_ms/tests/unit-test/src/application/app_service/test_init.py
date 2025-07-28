from unittest.mock import MagicMock, patch
from fastapi import FastAPI


class TestAppInitialization:
    """Test suite for verifying the FastAPI application initialization."""

    def test_app_initialization(self):
        """Test that the app is initialized correctly."""
        mock_app = MagicMock(spec=FastAPI)

        with patch(
            'src.infraestructure.entry_points.application.create_application',
            return_value=mock_app
        ):
            from src.applications.app_service import app
            assert app is mock_app

    def test_app_is_fastapi_instance(self):
        """Test that the app is actually a FastAPI instance."""
        from src.applications.app_service import app
        assert isinstance(app, FastAPI)
