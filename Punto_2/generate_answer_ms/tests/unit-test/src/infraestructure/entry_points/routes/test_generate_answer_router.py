import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from src.infraestructure.entry_points.routes.generate_answer_router import router as actual_router
from src.domain.model.answer.answer_model import GenerateAnswerRequest
from src.infraestructure.entry_points.fast_api.handlers.generate_answer_handler import GenerateAnswerHandler
from src.infraestructure.entry_points.routes.generate_answer_router import get_request_processor
from src.infraestructure.helpers.utils import verify_jwt
from src.applications.settings.container import get_deps_container
from fastapi import FastAPI

app = FastAPI()
app.include_router(actual_router)

@pytest.fixture(scope="module")
def app_with_mock_container():
    """
    Fixture to create a FastAPI app with a mocked container,
    ensuring 'app.container' is available at app startup.
    This fixture runs once per module.
    """
    app = FastAPI()
    mock_container = MagicMock()
    app.container = mock_container
    app.include_router(actual_router)
    return app

@pytest.fixture
def client(app_with_mock_container):
    """
    Fixture to create a TestClient for the configured app.
    """
    return TestClient(app_with_mock_container)

@pytest.fixture
def mock_improve_question_handler_instance():
    mock_improve_usecase = MagicMock()

    mock_handler = MagicMock(spec=GenerateAnswerHandler)
    mock_handler.improve_usecase = mock_improve_usecase
    mock_handler.generate = AsyncMock(return_value="mocked_result_from_handler")
    return mock_handler

def test_improve_question_route_success(
    client,
    mock_improve_question_handler_instance,
    monkeypatch
):
    mock_jwt_secret = "test_secret"
    mock_container_instance = MagicMock()
    mock_container_instance.jwt = mock_jwt_secret
    monkeypatch.setattr("src.applications.settings.container.get_deps_container", lambda: mock_container_instance)
    client.app.dependency_overrides[get_request_processor] = lambda: mock_improve_question_handler_instance
    client.app.dependency_overrides[verify_jwt] = lambda: {"user_id": "test_user"}

    try:
        sample_request_body = GenerateAnswerRequest(
            question="Hola soy una prueba", answer=[1, 2, 3]
        )
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cGxvYWQiLCJpYXQiOjE3NTM2NTg2Nzh9.xglAQJRpw4Aesqb8QLiUGvPMgsmndoQS7KY0-9fRhLs"}
        response = client.post("/generate_answer", json=sample_request_body.model_dump(), headers=headers)
        assert response.status_code == 200
        assert response.json() == {"answer": "mocked_result_from_handler"}
    finally:
        client.app.dependency_overrides = {}


def test_clean_split_route_unauthorized(client):
    with patch("src.infraestructure.entry_points.routes.generate_answer_router.verify_jwt", side_effect=HTTPException(status_code=401, detail="Unauthorized")):
        sample_request_body = GenerateAnswerRequest(
            question="Hola soy una prueba", answer=[1, 2, 3]
        )
        response = client.post("/generate_answer", json=sample_request_body.model_dump())
        assert response.status_code == 401
        assert response.json() == {"detail": "Missing or invalid Authorization header"}

