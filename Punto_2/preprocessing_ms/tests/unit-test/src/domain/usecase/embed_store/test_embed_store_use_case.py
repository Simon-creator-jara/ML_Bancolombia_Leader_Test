import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.domain.usecase.embed_store.embed_store_use_case import EmbedAndStoreUseCase


@pytest.fixture
def dummy_dataframe():
    data = {
        "title": ["Movie 1", "Movie 2"],
        "plot": ["This is a plot.", "Another plot."],
        "image": ["img1.jpg", "img2.jpg"],
        "text_to_embed": ["This is a plot.", "Another plot."]
    }
    return [pd.DataFrame(data)]


def test_embed_and_store_executes_correctly(dummy_dataframe):
    logger = MagicMock()
    mock_embedder = MagicMock()
    mock_embedder.embed_texts.return_value = [0.1] * 1536
    mock_repo = MagicMock()

    use_case = EmbedAndStoreUseCase(
        logger=logger,
        embedder=mock_embedder,
        repository=mock_repo,
        text_field="text_to_embed",
        batch_size=1,
        max_workers=2
    )

    result = use_case.execute(dummy_dataframe)

    assert result == "Upload Successful"
    assert mock_embedder.embed_texts.call_count > 0
    assert mock_repo.insert_chunks.call_count > 0
    mock_repo.insert_chunks.assert_called()
    logger.info.assert_any_call("Inserting in database")
