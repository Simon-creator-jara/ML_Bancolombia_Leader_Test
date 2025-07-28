from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.domain.model.dataset.dataset_model import (
    RawDataset
)
import pandas as pd


class DatasetCleaner(ABC):
    """Abstract interface for dataset cleaning and chunking processing."""

    @abstractmethod
    def __init__(self, config: Dict[str, Any], logger: Any):
        """Initialize the dataset cleaner with configuration and logger."""
        self.config = config
        self.logger = logger

    @abstractmethod
    async def process(
        self, inputs: RawDataset
    ) -> pd.DataFrame:
        """Process a batch of dataset records, performing cleaning and 
        chunking.

        Args:
            inputs: List of raw dataset records to be cleaned and chunked.

        Returns:
            List of processed dataset chunks ready for downstream embedding.
        """
        pass
