import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import HTTPException
from src.domain.model.embeddings.embeddings_model import question
from src.domain.usecase.embed_store.embed_store_use_case import EmbedAndStoreUseCase
from src.infraestructure.entry_points.fast_api.handlers.retrieve_handler import RetrieveDataHandler


@pytest.fixture
def mock_embed_use_case():
    return MagicMock(spec=EmbedAndStoreUseCase)


@pytest.fixture
def retrieve_data_handler(mock_embed_use_case):
    return RetrieveDataHandler(embed_use_case=mock_embed_use_case)


@pytest.mark.asyncio
async def test_handle_success(retrieve_data_handler, mock_embed_use_case):
    request = question(question="What is the meaning of life?")
    expected_embeddings = [0.1, 0.2, 0.3]

    mock_embed_use_case.execute = AsyncMock(return_value=expected_embeddings)

    result = await retrieve_data_handler.handle(request)

    mock_embed_use_case.execute.assert_called_once_with(request)
    assert result == expected_embeddings


@pytest.mark.asyncio
async def test_handle_file_not_found_error(retrieve_data_handler, mock_embed_use_case):
    request = question(question="What is the meaning of life?")

    mock_embed_use_case.execute = AsyncMock(side_effect=FileNotFoundError("File not found"))

    with pytest.raises(HTTPException) as exc_info:
        await retrieve_data_handler.handle(request)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "File not found"


@pytest.mark.asyncio
async def test_handle_generic_error(retrieve_data_handler, mock_embed_use_case):
    request = question(question="What is the meaning of life?")

    mock_embed_use_case.execute = AsyncMock(side_effect=Exception("Some internal error"))

    with pytest.raises(HTTPException) as exc_info:
        await retrieve_data_handler.handle(request)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error: Some internal error"
