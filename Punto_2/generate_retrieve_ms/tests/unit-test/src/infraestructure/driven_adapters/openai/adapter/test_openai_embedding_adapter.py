import pytest
from unittest.mock import MagicMock
from src.infraestructure.driven_adapters.openai.adapter.openai_embedding_adapter import OpenAIEmbeddingAdapter
from src.domain.model.embeddings.embeddings_model import question

def test_embed_texts_returns_embedding():
    mock_client = MagicMock()
    mock_embedding = [0.1, 0.2, 0.3]
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=mock_embedding)]
    mock_client.embeddings.create.return_value = mock_response

    adapter = OpenAIEmbeddingAdapter(mock_client)
    result = adapter.embed_texts(question(question="hello world"))

    assert result == mock_embedding
    mock_client.embeddings.create.assert_called_once_with(
        model="text-embedding-3-large",
        input="hello world"
    )

