import asyncio
from typing import List, Tuple
import numpy as np
import pandas as pd
from src.domain.model.database.gateway.database_gateway import ChunkRepository
from src.domain.model.embeddings.gateway.embeddings_gateway import EmbeddingGateway
from langchain.text_splitter import RecursiveCharacterTextSplitter
from concurrent.futures import ThreadPoolExecutor, as_completed


class EmbedAndStoreUseCase:
    def __init__(
        self,
        logger,
        embedder: EmbeddingGateway,
        repository: ChunkRepository,
        text_field: str = "text_to_embed",
        batch_size: int = 100,
        max_workers: int = 10,
        
    ):
        self.logger = logger
        self.embedder = embedder
        self.repo = repository
        self.text_field = text_field
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="text-embedding-3-large",
            chunk_size=1536,
            chunk_overlap=300
        )

    def _normalize(self, embedding: List[float]) -> List[float]:
        arr = np.array(embedding)
        norm = np.linalg.norm(arr)
        return (arr / norm).tolist() if norm > 0 else arr.tolist()

    def _process_single_chunk(self, title: str, plot: str, image: str, chunk_index: int, chunki: str) -> Tuple:
        embedding = self.embedder.embed_texts(chunki)
        if not isinstance(embedding, list):
            raise TypeError(f"Expected list from embedder.embed_texts, got {type(embedding)}")

        norm = self._normalize(embedding)
        return (title, chunk_index, chunki, plot, image, embedding, norm)

    def execute(self, df_chunks: List[pd.DataFrame]) -> str:
        batch = []

        for df_chunk in df_chunks:
            futures = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                for _, row in df_chunk.iterrows():
                    title = row["title"]
                    plot = str(row["plot"])
                    image = str(row["image"])
                    raw_text_to_embed = row[self.text_field]
                    self.logger.info(f"Inserting {title}")

                    if not raw_text_to_embed.strip():
                        continue

                    chunkis = self.splitter.split_text(raw_text_to_embed)

                    for i, chunki in enumerate(chunkis):
                        futures.append(executor.submit(self._process_single_chunk, title, plot, image, i, chunki))

                for future in as_completed(futures):
                    row_data = future.result()
                    if row_data:
                        batch.append(row_data)

                        if len(batch) >= self.batch_size:
                            self.logger.info("Inserting in database")
                            self.repo.insert_chunks(batch)
                            batch.clear()

        # Insert any remaining
        if batch:
            self.repo.insert_chunks(batch)

        return "Upload Successful"