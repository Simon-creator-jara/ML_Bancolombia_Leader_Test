import pytest
from unittest.mock import MagicMock, AsyncMock
from src.domain.model.embeddings.gateway.embeddings_gateway import EmbeddingGateway
from src.domain.model.database.gateway.database_gateway import ChunkRepository
from src.domain.model.embeddings.embeddings_model import question
from src.domain.usecase.embed_store.embed_store_use_case import EmbedAndStoreUseCase
import numpy as np

class DummyQuestion:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text
    
@pytest.mark.asyncio
async def test_embed_and_store_use_case_execute_success():
    mock_logger = MagicMock()
    mock_embedder = MagicMock()
    mock_repository = MagicMock()

    raw_embedding_for_normalization = [1.0, 1.0, 0.0]
    mock_embedder.embed_texts.return_value = raw_embedding_for_normalization
    mock_repository.insert_chunks.return_value = ["chunk_id_123"]

    use_case = EmbedAndStoreUseCase(mock_logger, mock_embedder, mock_repository)
    test_question = DummyQuestion(text="What is the capital of France?")

    result = await use_case.execute(test_question)

    mock_logger.info.assert_any_call(f"Received question: {test_question}")
    mock_logger.info.assert_any_call("iniciando normalizacion")
    mock_embedder.embed_texts.assert_called_once_with(test_question)

    expected_normalized_embedding = (np.array([1.0, 1.0, 0.0]) / np.linalg.norm(np.array([1.0, 1.0, 0.0]))).tolist()
    mock_repository.insert_chunks.assert_called_once()
    actual_inserted_embedding = mock_repository.insert_chunks.call_args[0][0]
    for i in range(len(expected_normalized_embedding)):
        assert actual_inserted_embedding[i] == pytest.approx(expected_normalized_embedding[i], rel=1e-6)

    assert result == ["chunk_id_123"]


@pytest.mark.asyncio
async def test_embed_and_store_use_case_normalize_zero_norm():
    mock_logger = MagicMock()
    mock_embedder = MagicMock()
    mock_repository = MagicMock()
    use_case = EmbedAndStoreUseCase(mock_logger, mock_embedder, mock_repository)

    zero_embedding = [0.0, 0.0, 0.0]

    normalized_embedding = await use_case._normalize(zero_embedding)

    assert normalized_embedding == [0.0, 0.0, 0.0]


@pytest.mark.asyncio
async def test_embed_and_store_use_case_execute_embedding_api_failure():
    mock_logger = MagicMock()
    mock_embedder = MagicMock()
    mock_repository = MagicMock()

    mock_embedder.embed_texts.side_effect = Exception("Embedding API error")

    use_case = EmbedAndStoreUseCase(mock_logger, mock_embedder, mock_repository)
    test_question = DummyQuestion(text="This should fail.")

    with pytest.raises(Exception, match="Embedding API error"):
        await use_case.execute(test_question)

    mock_repository.insert_chunks.assert_not_called()
    mock_logger.info.assert_any_call(f"Received question: {test_question}")
    mock_logger.info.assert_called_once()


@pytest.mark.asyncio
async def test_embed_and_store_use_case_execute_repository_insertion_failure():
    mock_logger = MagicMock()
    mock_embedder = MagicMock()
    mock_repository = MagicMock()

    mock_embedder.embed_texts.return_value = [0.1, 0.2, 0.3]

    mock_repository.insert_chunks.side_effect = Exception("Database insertion error")

    use_case = EmbedAndStoreUseCase(mock_logger, mock_embedder, mock_repository)
    test_question = DummyQuestion(text="This should also fail.")

    with pytest.raises(Exception, match="Database insertion error"):
        await use_case.execute(test_question)

    mock_embedder.embed_texts.assert_called_once()
    mock_logger.info.assert_any_call(f"Received question: {test_question}")
    mock_logger.info.assert_any_call("iniciando normalizacion")
    mock_repository.insert_chunks.assert_called_once()