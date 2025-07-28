import pytest
from unittest.mock import AsyncMock, MagicMock
from src.domain.usecase.improve_question.improve_question_use_case import ImproveQuestionUseCase
from src.domain.model.question.question_model import question
from src.domain.model.message_error.message_error_model import MessageError

@pytest.mark.asyncio
async def test_execute_success():
    mock_gateway = AsyncMock()
    mock_gateway.improve.return_value = "improved"
    mock_sns = AsyncMock()
    mock_logger = MagicMock()
    uc = ImproveQuestionUseCase(mock_gateway, mock_sns, mock_logger)
    q = question(question="Original?")
    result = await uc.execute(q)
    assert result == "improved"
    mock_logger.info.assert_called_once_with("Improving question")
    mock_sns.send.assert_not_called()

@pytest.mark.asyncio
async def test_execute_failure():
    mock_gateway = AsyncMock()
    mock_gateway.improve.side_effect = Exception("fail")
    mock_sns = AsyncMock()
    mock_logger = MagicMock()
    uc = ImproveQuestionUseCase(mock_gateway, mock_sns, mock_logger)
    q = question(question="Original?")
    with pytest.raises(Exception) as exc:
        await uc.execute(q)
    assert "fail" in str(exc.value)
    mock_logger.info.assert_called_once_with("Improving question")
    mock_logger.error.assert_called_once()
    sent = mock_sns.send.call_args[0][0]
    assert isinstance(sent, MessageError)
    assert sent.subject_message == "Error executing DataCleaner"
    assert sent.content_message == "Error Details: fail"
