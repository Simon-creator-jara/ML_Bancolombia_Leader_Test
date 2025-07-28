from fastapi import APIRouter

from src.infraestructure.entry_points.routes import clean_split_router
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
        clean_split_router.router, prefix="/clean", tags=["clean"]
    )
    return api_router
