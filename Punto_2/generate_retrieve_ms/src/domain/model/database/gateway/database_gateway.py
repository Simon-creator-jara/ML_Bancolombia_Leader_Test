from abc import ABC, abstractmethod
from typing import List, Tuple


class ChunkRepository(ABC):
    """
    Gateway interface for persisting chunk records.
    """

    @abstractmethod
    def insert_chunks(self, records: List[float]) -> None:
        """
        Persist a batch of chunk tuples.

        Each tuple must correspond to:
        (title, chunk_id, chunk_text, plot, image, embedding, embedding_normalized)
        """
        pass
