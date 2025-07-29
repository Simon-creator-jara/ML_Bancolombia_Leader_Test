from typing import TYPE_CHECKING, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from asyncpg import create_pool
from src.domain.model.embeddings.embeddings_model import question
from src.infraestructure.entry_points.fast_api.handlers.retrieve_handler import RetrieveDataHandler
from src.infraestructure.helpers.utils import verify_jwt

if TYPE_CHECKING:
    from src.applications.settings.container import Container

router = APIRouter()


async def get_request_processor(request: Request) -> RetrieveDataHandler:

    container: "Container" = request.app.container
    return RetrieveDataHandler(
        embed_use_case=container.embed_store_use_case
    )


@router.post("/retrieve_data", response_model=Dict[str, List])
async def retrieve_route(
    request: question,
    handler: RetrieveDataHandler = Depends(get_request_processor),
    payload: dict = Depends(verify_jwt)
):
    return {"answer": await handler.handle(request)}
