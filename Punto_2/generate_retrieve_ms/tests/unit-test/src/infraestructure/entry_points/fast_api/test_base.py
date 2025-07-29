import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

import src.infraestructure.entry_points.fast_api.base as routes_module


@pytest.fixture(autouse=True)
def dummy_sub_routers(monkeypatch):
    health = APIRouter()
    @health.get("/ping", tags=["health"])
    async def ping():
        return {"ping": "pong"}

    retrieve = APIRouter()
    @retrieve.post("/run", tags=["retrieve"])
    async def run():
        return {"run": True}

    monkeypatch.setattr(routes_module.health_router, "router", health)
    monkeypatch.setattr(routes_module.retrieve_router, "router", retrieve)

    yield


def test_set_routes_includes_both_subrouters_under_prefix():
    api_router = routes_module.set_routes(prefix="/api/v1")

    app = FastAPI()
    app.include_router(api_router)
    client = TestClient(app)
    resp = client.get("/api/v1/health/ping")
    assert resp.status_code == 200
    assert resp.json() == {"ping": "pong"}

    resp = client.post("/api/v1/retrieve/run")
    assert resp.status_code == 200
    assert resp.json() == {"run": True}

