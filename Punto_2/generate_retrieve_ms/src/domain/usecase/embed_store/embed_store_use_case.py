import asyncio
from typing import List, Tuple
import numpy as np
from src.domain.model.embeddings.gateway.embeddings_gateway import EmbeddingGateway
from src.domain.model.database.gateway.database_gateway import ChunkRepository
from src.domain.model.embeddings.embeddings_model import question


class EmbedAndStoreUseCase:
    def __init__(
        self,
        logger,
        embedder: EmbeddingGateway,
        repository: ChunkRepository
    ):
        self.logger = logger
        self.embedder = embedder
        self.repo = repository

    async def _normalize(self, embedding: List[float]) -> List[float]:
        arr = np.array(embedding)
        norm = np.linalg.norm(arr)
        return (arr / norm).tolist() if norm > 0 else arr.tolist()

    async def execute(self, question: question) -> List:
        self.logger.info(f"Received question: {question}")
        raw_embedding = await asyncio.to_thread(self.embedder.embed_texts, question)
        self.logger.info(f"iniciando normalizacion")
        normalization = await self._normalize(raw_embedding)
        return await asyncio.to_thread(self.repo.insert_chunks, normalization)
