from src.domain.model.message_error.message_error_model import MessageError
from src.domain.model.answer.gateway.generate_answer_repository import GenerateAnswerGateway
from src.domain.model.message_error.gateways.message_error_repository import MessageErrorRepository
from src.domain.model.answer.answer_model import answer


class GenerateAnswerUseCase:
    def __init__(self, gateway: GenerateAnswerGateway, sns_notifier: MessageErrorRepository, logger):
        self.gateway = gateway
        self.sns_notifier = sns_notifier
        self.logger = logger

    async def execute(self, question: str, answer: answer) -> str:
        try:
            self.logger.info("Improving question")
            return await self.gateway.generate(question, answer)
        except Exception as error:
            self.logger.error(f"Error reading file: {error}")
            error_message = f"Error Details: {error}"
            subject_message = ("Error executing GenerateAnswerUseCase")
            message_error = MessageError(subject_message=subject_message,
                                         content_message=error_message)
            await self.sns_notifier.send(message_error)
            raise
