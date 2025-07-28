from typing import TYPE_CHECKING, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Request
from src.domain.model.question.question_model import question
from src.infraestructure.entry_points.fast_api.handlers.improve_question_handler import ImproverQuestionHandler
from src.infraestructure.helpers.utils import verify_jwt

if TYPE_CHECKING:
    from src.applications.settings.container import Container

router = APIRouter()


async def get_request_processor(request: Request) -> ImproverQuestionHandler:

    container: "Container" = request.app.container
    return ImproverQuestionHandler(
        improve_usecase=container.improver_use_case,
        logger=container.logger
    )


@router.post("/improve_question", response_model=Dict[str, str])
async def clean_split_route(
    request: question,
    handler: ImproverQuestionHandler = Depends(get_request_processor),
    payload: dict = Depends(verify_jwt)
):
    return {"answer": await handler.improve(request)}
