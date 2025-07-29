from abc import ABC, abstractmethod
from typing import List
from src.domain.model.embeddings.embeddings_model import question


class EmbeddingGateway(ABC):
    """
    Gateway interface for generating text embeddings.
    """

    @abstractmethod
    def embed_texts(self, texts: question) -> List:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of input strings
        Returns:
            List of embedding vectors (one per input)
        """
        pass
