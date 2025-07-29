import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from src.infraestructure.entry_points.fast_api.handlers.generate_answer_handler import GenerateAnswerHandler
from src.domain.model.answer.answer_model import GenerateAnswerRequest
from src.domain.usecase.generate_answer.generate_answer_use_case import GenerateAnswerUseCase


@pytest.mark.asyncio
async def test_generate_success():
    mock_usecase = AsyncMock(spec=GenerateAnswerUseCase)
    mock_usecase.execute.return_value = "This is the generated answer."

    mock_logger = MagicMock()

    handler = GenerateAnswerHandler(mock_usecase, mock_logger)

    request_data = GenerateAnswerRequest(question="What is the capital?", answer=["context data 1", "context data 2"])

    result = await handler.generate(request_data)

    mock_logger.info.assert_called_once_with("Procesando pregunta")

    mock_usecase.execute.assert_awaited_once_with(request_data.question, request_data.answer)

    assert result == "This is the generated answer."


@pytest.mark.asyncio
async def test_generate_file_not_found_error():
    mock_usecase = AsyncMock(spec=GenerateAnswerUseCase)
    mock_usecase.execute.side_effect = FileNotFoundError("File not found for processing.")

    mock_logger = MagicMock()

    handler = GenerateAnswerHandler(mock_usecase, mock_logger)
    request_data = GenerateAnswerRequest(question="Nonexistent file?", answer=[])

    with pytest.raises(HTTPException) as exc_info:
        await handler.generate(request_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "File not found for processing."

    mock_logger.info.assert_called_once_with("Procesando pregunta")
    mock_usecase.execute.assert_awaited_once_with(request_data.question, request_data.answer)
    mock_logger.error.assert_not_called()
