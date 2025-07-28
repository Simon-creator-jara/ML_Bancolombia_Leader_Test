import asyncio
import pandas as pd
from typing import List
from fastapi import HTTPException
from src.domain.model.dataset.dataset_model import RawDataset
from src.domain.usecase.clean_data.clean_data_use_case import \
    DatasetCleanerImpl
from src.domain.usecase.split_data.split_data_use_case import SplitterImpl
from src.domain.usecase.embed_store.embed_store_use_case import EmbedAndStoreUseCase


class CleanDataHandler:
    def __init__(self, cleaner_usecase: DatasetCleanerImpl,
                 splitter_usecase: SplitterImpl,
                 embed_use_case: EmbedAndStoreUseCase):
        """
        Initialize the handler with the dataset cleaner and optional splitter.

        Args:
            cleaner_usecase: DatasetCleanerImpl instance
            splitter_usecase: SplitterImpl instance (optional)
        """
        self.cleaner = cleaner_usecase
        self.splitter = splitter_usecase
        self.embed_use_case = embed_use_case

    async def handle(self, request: RawDataset,
                     chunk_size: int = 100) -> List[dict]:
        """
        Handle a dataset cleaning request and return cleaned + chunked dataset.

        Args:
            request: RawDataset containing file_path.
            chunk_size: number of rows per chunk.

        Returns:
            ChunkedDataset response.
        """
        try:
            cleaned_df = await self.cleaner.process(request)

            if self.splitter is None:
                raise HTTPException(
                    status_code=500,
                    detail="Splitter use case is not configured."
                )

            chunked_dataset = await self.splitter.split(cleaned_df, chunk_size)
            await asyncio.to_thread(self.embed_use_case.execute,chunked_dataset)

        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}") from e
