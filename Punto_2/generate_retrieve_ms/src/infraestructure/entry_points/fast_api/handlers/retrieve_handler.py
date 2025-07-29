import asyncio
from typing import List
from fastapi import HTTPException
from src.domain.model.embeddings.embeddings_model import question
from src.domain.usecase.embed_store.embed_store_use_case import EmbedAndStoreUseCase


class RetrieveDataHandler:
    def __init__(self, embed_use_case: EmbedAndStoreUseCase):
        self.embed_use_case = embed_use_case

    async def handle(self, request: question) -> List:
        try:
            embeddings = await self.embed_use_case.execute(request)
            return embeddings
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}") from e
