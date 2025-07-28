"""Error handling module for s3 repository."""
from src.domain.model.message_error.gateways.message_error_repository import (
    MessageErrorRepository,
)


class S3RepositoryError(MessageErrorRepository):
    """ Class to handle errors for Model """

    async def send(self, message: str) -> None:
        """Send an error message."""

    def __str__(self):
        """ Message detail error """
        return f"[Model Error] {self.message or 'No details.'}"
