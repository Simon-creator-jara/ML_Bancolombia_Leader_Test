import asyncio
import logging
import uuid
import threading
from datetime import datetime
from typing import Callable, Awaitable, Optional, Union, Any, Dict
import inspect

_tasks: Dict[str, threading.Thread] = {}
_results: Dict[str, Any] = {}


async def execute_task(task_id: str, func: Union[Callable[..., Awaitable], Awaitable], *args, **kwargs):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Iniciando tarea {task_id} a las {start_time}")

    try:
        if inspect.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        elif inspect.isawaitable(func):
            result = await func
        else:
            raise TypeError(
                f"Func debe ser async o awaitable, recibido: {type(func)}")

        _results[task_id] = {
            'success': True,
            'result': result,
            'start_time': start_time,
            'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        logging.info(f"Tarea {task_id} completada exitosamente")

    except Exception as e:
        logging.error(f"Error en tarea {task_id}: {str(e)}")
        import traceback
        traceback.print_exc()

        _results[task_id] = {
            'success': False,
            'error': str(e),
            'start_time': start_time,
            'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    finally:
        _tasks.pop(task_id, None)


def start_task(func: Union[Callable[..., Awaitable], Awaitable], *args, **kwargs) -> str:
    task_id = str(uuid.uuid4())

    def run_async_task():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(execute_task(
                task_id, func, *args, **kwargs))
        except Exception as e:
            logging.error(f"Error en hilo de tarea {task_id}: {str(e)}")
            _results[task_id] = {
                'success': False,
                'error': str(e),
                'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    thread = threading.Thread(target=run_async_task, daemon=True)
    thread.start()
    _tasks[task_id] = thread

    logging.info(f"Tarea {task_id} iniciada en nuevo hilo")
    return task_id


def get_task_status(task_id: str) -> str:
    if task_id in _tasks:
        thread = _tasks[task_id]
        if thread.is_alive():
            return 'In progress'
        elif task_id not in _results:
            return 'Error'

    if task_id in _results:
        return 'Completed' if _results[task_id].get('success', False) else 'Error'

    return 'Not Found'


def get_task_result(task_id: str) -> Optional[Dict[str, Any]]:
    try:
        result_data = _results.get(task_id)
        if not result_data:
            return None

        serializable_result = {}
        for key, value in result_data.items():
            if key == 'result' and not isinstance(value, (str, int, float, bool, dict, list, tuple, type(None))):
                if hasattr(value, 'to_dict'):
                    serializable_result[key] = value.to_dict()
                else:
                    serializable_result[key] = str(value)
            elif isinstance(value, dict):
                serializable_dict = {k: str(v) if not isinstance(
                    v, (str, int, float, bool, dict, list, tuple, type(None))) else v for k, v in value.items()}
                serializable_result[key] = serializable_dict
            else:
                serializable_result[key] = value

        return serializable_result

    except Exception as e:
        logging.error(
            f"Error al serializar resultado de tarea {task_id}: {str(e)}")
        return {'success': False, 'error': f"Error al obtener resultado: {str(e)}"}
