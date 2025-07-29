from typing import TYPE_CHECKING, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Request
from src.domain.model.answer.answer_model import answer
from src.domain.model.answer.answer_model import GenerateAnswerRequest
from src.infraestructure.entry_points.fast_api.handlers.generate_answer_handler import GenerateAnswerHandler
from src.infraestructure.helpers.utils import verify_jwt

if TYPE_CHECKING:
    from src.applications.settings.container import Container

router = APIRouter()


async def get_request_processor(request: Request) -> GenerateAnswerHandler:

    container: "Container" = request.app.container
    return GenerateAnswerHandler(
        generate_answer_usecase=container.generate_answer_usecase,
        logger=container.logger
    )


@router.post("/generate_answer", response_model=Dict[str, str])
async def genrate_answer_route(
    request: GenerateAnswerRequest,
    handler: GenerateAnswerHandler = Depends(get_request_processor),
    payload: dict = Depends(verify_jwt)
):
    return {"answer": await handler.generate(request)}
