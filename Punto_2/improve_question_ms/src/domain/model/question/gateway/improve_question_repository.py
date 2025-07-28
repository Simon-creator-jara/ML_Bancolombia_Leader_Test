from abc import ABC, abstractmethod


class QuestionImproverGateway(ABC):
    @abstractmethod
    def __init__(self, logger):
        self.logger = logger

    async def improve(self, question: str) -> str:
        """Given a question, return the improved/rephrased version."""
        pass
