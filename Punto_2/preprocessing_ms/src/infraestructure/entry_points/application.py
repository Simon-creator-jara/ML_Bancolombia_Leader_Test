from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.applications.settings.container import get_deps_container
from src.infraestructure.entry_points.fast_api.base import set_routes


def include_router(app: FastAPI, prefix: str = ""):
    """Include all routes in the FastAPI application."""
    app.include_router(set_routes(prefix))


def create_application():
    """Create a FastAPI application with all routes."""
    container = get_deps_container()
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.container = container
    include_router(app, prefix=container.app_config.url_prefix)
    return app
