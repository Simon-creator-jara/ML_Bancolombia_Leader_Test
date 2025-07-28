import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import AsyncMock, patch, MagicMock
from src.infraestructure.helpers.task_manager import start_task
from src.infraestructure.helpers.task_manager import get_task_status, get_task_result
from src.domain.model.dataset.dataset_model import RawDataset
from src.infraestructure.entry_points.routes.clean_split_router import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)


@pytest.fixture
def sample_dataset():
    return RawDataset(
        file_path="path/to/sample.csv",
        source="test",
        metadata={"user": "tester"}
    )


import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
# Assuming your router is now at src.infraestructure.entry_points.routes.clean_split_router
from src.infraestructure.entry_points.routes.clean_split_router import router as actual_router
from src.domain.model.dataset.dataset_model import RawDataset
from src.infraestructure.entry_points.fast_api.handlers.clean_split_data_handler import CleanDataHandler

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
def mock_clean_data_handler_instance():
    mock_cleaner_usecase = MagicMock()
    mock_splitter_usecase = MagicMock()
    mock_embed_use_case = MagicMock()

    mock_handler = MagicMock(spec=CleanDataHandler)
    mock_handler.cleaner_usecase = mock_cleaner_usecase
    mock_handler.splitter_usecase = mock_splitter_usecase
    mock_handler.embed_use_case = mock_embed_use_case
    mock_handler.handle.return_value = "mocked_result_from_handler"
    return mock_handler



@pytest.fixture
def mock_start_task():
    return MagicMock(return_value="mock_task_id_123")


def test_clean_split_route_success(
    client, # Use the client fixture
    mock_clean_data_handler_instance,
    mock_start_task
):
    with patch("src.infraestructure.entry_points.routes.clean_split_router.get_request_processor", return_value=mock_clean_data_handler_instance), \
         patch("src.infraestructure.helpers.task_manager.start_task", new=mock_start_task):
        sample_request_body = RawDataset(
            file_path="path/to/test_file.csv"
        )
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cGxvYWQiLCJpYXQiOjE3NTM2NTg2Nzh9.xglAQJRpw4Aesqb8QLiUGvPMgsmndoQS7KY0-9fRhLs"}
        response = client.post("/clean_split", json=sample_request_body.model_dump(), headers=headers)

        assert response.status_code == 200


def test_clean_split_route_unauthorized(client):
    with patch("src.infraestructure.entry_points.routes.clean_split_router.verify_jwt", side_effect=HTTPException(status_code=401, detail="Unauthorized")):
        sample_request_body = RawDataset(
            file_path="path/to/test_file.csv"
        )
        response = client.post("/clean_split", json=sample_request_body.model_dump())
        assert response.status_code == 401
        assert response.json() == {"detail": "Missing or invalid Authorization header"}

@patch("src.infraestructure.entry_points.routes.clean_split_router.get_task_status", return_value="Completed")
def test_verificar_estado_ok(mock_get_status):
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/status/abc123")
    assert response.status_code == 200
    assert response.json() == {"status": "Completed"}

@patch("src.infraestructure.entry_points.routes.clean_split_router.get_task_result", return_value={"output": "Done"})
def test_obtener_resultado_ok(mock_get_result):
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/result/abc123")
    assert response.status_code == 200
    assert response.json() == {"result": {"output": "Done"}}
