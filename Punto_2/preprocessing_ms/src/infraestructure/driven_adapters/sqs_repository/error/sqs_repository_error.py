"""Error handling module for sqs repository."""
from src.domain.model import MessageErrorRepository


class SqsRepositoryError(MessageErrorRepository):
    """ Class to handle errors for Model """

    async def send(self, message):
        """ Send error message """

    def __str__(self):
        """ Message detail error """
        return f"[Model Error] {self.message or 'No details.'}"
