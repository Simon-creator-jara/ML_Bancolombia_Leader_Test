import pytest
import threading
from types import SimpleNamespace
from datetime import datetime
import time

from src.infraestructure.helpers.task_manager import (
    execute_task,
    start_task,
    get_task_status,
    get_task_result,
    _tasks,
    _results,
)


@pytest.fixture(autouse=True)
def clear_state():
    _tasks.clear()
    _results.clear()
    yield
    _tasks.clear()
    _results.clear()


@pytest.mark.asyncio
async def test_execute_task_success():
    async def dummy_add(x, y):
        return x + y

    task_id = "task-success"
    await execute_task(task_id, dummy_add, 2, 3)
    assert task_id in _results
    res = _results[task_id]
    assert res["success"] is True
    assert res["result"] == 5
    assert "start_time" in res and "end_time" in res


@pytest.mark.asyncio
async def test_execute_task_exception():
    async def bad():
        raise ValueError("kaboom")

    task_id = "task-fail"
    await execute_task(task_id, bad)
    assert task_id in _results
    res = _results[task_id]
    assert res["success"] is False
    assert "kaboom" in res["error"]


def test_get_task_status_variations():
    class Alive:
        def is_alive(self): return True
    _tasks["t1"] = Alive()
    assert get_task_status("t1") == "In progress"
    class Dead:
        def is_alive(self): return False
    _tasks["t2"] = Dead()
    assert get_task_status("t2") == "Error"
    _results["t3"] = {"success": True}
    assert get_task_status("t3") == "Completed"
    _results["t4"] = {"success": False}
    assert get_task_status("t4") == "Error"
    assert get_task_status("no-such") == "Not Found"


def test_get_task_result_serialization():
    class WithDict:
        def to_dict(self): return {"foo": 42}
    _results["r1"] = {
        "success": True,
        "result": WithDict(),
        "start_time": "A",
        "end_time": "B",
    }
    out1 = get_task_result("r1")
    assert out1["result"] == {"foo": 42}
    class NoDict: pass
    _results["r2"] = {
        "success": True,
        "result": NoDict(),
        "start_time": "A",
        "end_time": "B",
    }
    out2 = get_task_result("r2")
    assert isinstance(out2["result"], str)
    _results["r3"] = {
        "success": True,
        "result": {"x": NoDict()},
        "start_time": "A",
        "end_time": "B",
    }
    out3 = get_task_result("r3")
    assert isinstance(out3["result"]["x"], str)


def test_start_task_runs_in_background_and_records_result(monkeypatch):
    class FakeThread:
        def __init__(self, target, daemon):
            self._target = target
        def start(self):
            # run synchronously
            self._target()
        def is_alive(self):
            return False

    monkeypatch.setattr(threading, "Thread", FakeThread)
    async def mul(x):
        return x * 3
    task_id = start_task(mul(5))
    assert get_task_status(task_id) == "Completed"
    res = get_task_result(task_id)
    assert res["result"] == 15
