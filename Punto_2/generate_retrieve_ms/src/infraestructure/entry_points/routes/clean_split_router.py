from typing import TYPE_CHECKING, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from asyncpg import create_pool
from src.domain.model.dataset.dataset_model import RawDataset
from src.infraestructure.entry_points.fast_api.handlers.\
    clean_split_data_handler import CleanDataHandler
from src.infraestructure.helpers.task_manager import start_task
from src.infraestructure.helpers.task_manager import get_task_status, get_task_result
from src.infraestructure.helpers.utils import verify_jwt

if TYPE_CHECKING:
    from src.applications.settings.container import Container

router = APIRouter()


async def get_request_processor(request: Request) -> CleanDataHandler:

    container: "Container" = request.app.container
    return CleanDataHandler(
        cleaner_usecase=container.dataset_cleaner_use_case,
        splitter_usecase=container.splitter_use_case,
        embed_use_case=container.embed_store_use_case
    )


@router.post("/clean_split", response_model=Dict[str, str])
async def clean_split_route(
    request: RawDataset,
    handler: CleanDataHandler = Depends(get_request_processor),
    payload: dict = Depends(verify_jwt)
):
    task_id = start_task(handler.handle, request, 100)
    return {"task_id": task_id}


@router.get("/status/{task_id}", tags=["clean"], response_model=dict)
def verificar_estado(
    task_id: str
):
    """Verifica el estado de una tarea específica."""
    try:
        status = get_task_status(task_id)
        if status == "Not Found":
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/result/{task_id}", tags=["clean"], response_model=dict)
def obtener_resultado(
    task_id: str
):
    """Obtiene el resultado de una tarea específica."""
    try:
        result = get_task_result(task_id)
        if result == "Not Found":
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
