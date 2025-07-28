from abc import ABC, abstractmethod
from typing import List


class EmbeddingGateway(ABC):
    """
    Gateway interface for generating text embeddings.
    """

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of input strings
        Returns:
            List of embedding vectors (one per input)
        """
        pass
