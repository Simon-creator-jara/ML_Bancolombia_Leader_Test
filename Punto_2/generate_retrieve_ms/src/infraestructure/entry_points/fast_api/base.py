from fastapi import APIRouter

from src.infraestructure.entry_points.routes import retrieve_router
from src.infraestructure.entry_points.routes import (
    health_router
)


def set_routes(prefix: str):
    """Set all routes in the FastAPI application."""
    api_router = APIRouter(prefix=prefix)
    api_router.include_router(
        health_router.router, prefix="/health", tags=["health"]
    )
    api_router.include_router(
        retrieve_router.router, prefix="/retrieve", tags=["retrieve"]
    )
    return api_router
