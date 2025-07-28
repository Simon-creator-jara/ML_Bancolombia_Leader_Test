import asyncio
from fastapi import HTTPException
from src.domain.usecase.improve_question.improve_question_use_case import ImproveQuestionUseCase
from src.domain.model.question.question_model import question


class ImproverQuestionHandler:
    def __init__(self, improve_usecase: ImproveQuestionUseCase, logger):
        self.improver = improve_usecase
        self.logger = logger

    async def improve(self, request: question) -> str:
        try:
            self.logger.info("Procesando pregunta")
            resultado = await self.improver.execute(request)
            return resultado
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}") from e
