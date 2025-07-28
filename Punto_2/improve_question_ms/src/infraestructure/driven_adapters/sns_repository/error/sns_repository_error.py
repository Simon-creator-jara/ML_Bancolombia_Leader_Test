"""Error handling module for sns repository."""
from src.domain.model import MessageErrorRepository


class SnsRepositoryError(MessageErrorRepository):
    """ Class to handle errors for Model """

    async def send(self, message):
        """ Override the abstract send method """

    def __str__(self):
        """ Message detail error """
        return f"[Model Error] {self.message or 'No details.'}"
