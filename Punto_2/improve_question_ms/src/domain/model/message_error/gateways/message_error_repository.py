"Message gateway definition."
import abc
from src.domain.model.message_error.message_error_model import MessageError


class MessageErrorRepository(Exception):
    "Message repository gateways."
    def __init__(self, **kwargs):
        self.message = kwargs.get("message", None)
        self.type = kwargs.get("type", None)

    def __str__(self):
        """ Message detail error """
        return f"[RepositoryError] {self.message or 'No details.'}"

    @abc.abstractmethod
    async def send(self, message: MessageError):
        """send method to be implemented."""
