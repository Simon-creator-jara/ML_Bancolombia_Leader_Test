from fastapi import FastAPI

from src.applications.settings.container import get_deps_container
from src.infraestructure.entry_points.fast_api.base import set_routes


def include_router(app: FastAPI, prefix: str = ""):
    """Include all routes in the FastAPI application."""
    app.include_router(set_routes(prefix))


def create_application():
    """Create a FastAPI application with all routes."""
    container = get_deps_container()
    app = FastAPI()
    app.container = container
    include_router(app, prefix=container.app_config.url_prefix)
    return app
