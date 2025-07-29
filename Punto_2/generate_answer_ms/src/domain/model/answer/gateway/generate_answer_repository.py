from abc import ABC, abstractmethod
from src.domain.model.answer.answer_model import answer

class GenerateAnswerGateway(ABC):
    @abstractmethod
    def __init__(self, logger):
        self.logger = logger

    async def generate(self, question: str, answer: answer) -> str:
        """Given a question, return the improved/rephrased version."""
        pass
