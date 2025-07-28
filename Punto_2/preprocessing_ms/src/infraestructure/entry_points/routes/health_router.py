from typing import Annotated, TYPE_CHECKING
from fastapi import APIRouter, Depends, Request
from src.domain.usecase import CheckHealthUseCase
from ..fast_api.handlers.health_handler import (
    HealthHandler
)

if TYPE_CHECKING:
    from src.applications.settings.container import Container

router = APIRouter()


async def get_health_usecase(request: Request):
    """Get health use case."""
    container: "Container" = request.app.container
    return container.check_health_use_case


HealthCheckUseCaseDep = Annotated[
    CheckHealthUseCase, Depends(get_health_usecase)
]


@router.get("", tags=["health"])
async def health_check_route(health_check_use_case: HealthCheckUseCaseDep):
    """Health check route."""
    handler = HealthHandler(health_check_use_case)
    return await handler.check()
