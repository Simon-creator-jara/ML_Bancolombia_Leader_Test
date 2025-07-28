import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from src.infraestructure.entry_points.fast_api.handlers.improve_question_handler import ImproverQuestionHandler
from src.domain.model.question.question_model import question

@pytest.mark.asyncio
async def test_improve_success():
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = "Mejorada"
    mock_logger = MagicMock()
    handler = ImproverQuestionHandler(mock_usecase, mock_logger)
    req = question(question="¿Cuál es tu nombre?")
    result = await handler.improve(req)
    assert result == "Mejorada"
    mock_logger.info.assert_called_once_with("Procesando pregunta")
    mock_usecase.execute.assert_awaited_once_with(req)
