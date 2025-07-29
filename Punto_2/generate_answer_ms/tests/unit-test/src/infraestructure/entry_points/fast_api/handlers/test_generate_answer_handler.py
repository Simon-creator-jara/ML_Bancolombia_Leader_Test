import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from src.infraestructure.entry_points.fast_api.handlers.generate_answer_handler import GenerateAnswerHandler
from src.domain.model.answer.answer_model import GenerateAnswerRequest

@pytest.mark.asyncio
async def test_improve_success():
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = "Mejorada"
    mock_logger = MagicMock()
    handler = GenerateAnswerHandler(mock_usecase, mock_logger)
    req = GenerateAnswerRequest(question="¿Cuál es tu nombre?", answer=[1, 2, 3])
    result = await handler.generate(req)
    assert result == "Mejorada"
    mock_logger.info.assert_called_once_with("Procesando pregunta")
    mock_usecase.execute.assert_awaited_once_with(req.question, req.answer)
