from abc import ABC, abstractmethod
from typing import Dict, Any
from src.domain.model.repository.repository_model import GetJson, SaveJson


class OCRRepositoryGateway(ABC):
    """OCR Repository Gateway interface."""

    @abstractmethod
    def __init__(self, config: Dict[str, Any], logger):
        self.logger = logger
        self.config = config

    @abstractmethod
    def get_json(self, s3_path: GetJson) -> Dict:
        """Get OCR jsons"""
        pass

    @abstractmethod
    def save_json(self, bucket: str, key: str, data: SaveJson) -> str:
        """Save OCR jsons"""
        pass
