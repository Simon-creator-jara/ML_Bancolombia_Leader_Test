from abc import ABC, abstractmethod
from typing import List
import pandas as pd


class Splitter(ABC):
    """Abstract interface for queue messaging services."""

    @abstractmethod
    def __init__(self, logger):
        self.logger = logger

    async def split(self, df: pd.DataFrame, chunk_size: int) -> List[pd.DataFrame]:
        """Split the dataframe in small chunks.

        Args:
            df: Dataframe to split.
            chunk_size: size of each chunk.

        Returns:
            ChunkedDataset
        """
        pass
