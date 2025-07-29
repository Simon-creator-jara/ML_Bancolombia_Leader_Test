import asyncio
from fastapi import HTTPException
from src.domain.usecase.generate_answer.generate_answer_use_case import GenerateAnswerUseCase
from src.domain.model.answer.answer_model import GenerateAnswerRequest


class GenerateAnswerHandler:
    def __init__(self, generate_answer_usecase: GenerateAnswerUseCase, logger):
        self.generator = generate_answer_usecase
        self.logger = logger

    async def generate(self, request: GenerateAnswerRequest) -> str:
        try:
            self.logger.info("Procesando pregunta")
            resultado = await self.generator.execute(request.question, request.answer)
            return resultado
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}") from e
