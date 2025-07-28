import pytest
import pandas as pd
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from src.infraestructure.entry_points.fast_api.handlers.clean_split_data_handler import CleanDataHandler
from src.domain.model.dataset.dataset_model import RawDataset

@pytest.mark.asyncio
async def test_handle_success():
    mock_cleaner = AsyncMock()
    mock_splitter = AsyncMock()
    mock_embed = MagicMock()
    
    df = pd.DataFrame({"title": ["Movie"], "plot": ["A plot"], "image": ["img.jpg"]})
    mock_cleaner.process.return_value = df
    mock_splitter.split.return_value = [df]
    
    handler = CleanDataHandler(
        cleaner_usecase=mock_cleaner,
        splitter_usecase=mock_splitter,
        embed_use_case=mock_embed
    )
    
    request = RawDataset(file_path="dummy.csv")
    await handler.handle(request)
    
    mock_cleaner.process.assert_called_once_with(request)
    mock_splitter.split.assert_called_once_with(df, 100)
    mock_embed.execute.assert_called_once_with([df])
