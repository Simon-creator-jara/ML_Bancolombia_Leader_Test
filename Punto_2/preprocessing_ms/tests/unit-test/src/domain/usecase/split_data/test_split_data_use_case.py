import pytest
import pandas as pd
from types import SimpleNamespace

# Replace this with the actual path to your SplitterImpl
from src.domain.usecase.split_data.split_data_use_case import SplitterImpl
from src.domain.model.message_error.message_error_model import MessageError


class DummySNS:
    def __init__(self):
        self.sent = []

    async def send(self, message_error: MessageError):
        self.sent.append(message_error)


@pytest.fixture
def logger():
    # simple stub logger
    return SimpleNamespace(info=lambda *a, **k: None, error=lambda *a, **k: None)


@pytest.fixture
def sns_notifier():
    return DummySNS()


@pytest.fixture
def splitter(logger, sns_notifier):
    return SplitterImpl(logger=logger, sns_notifier=sns_notifier)


@pytest.mark.asyncio
async def test_split_success(splitter):
    # Given a DataFrame of 4 rows...
    df = pd.DataFrame({"x": [1, 2, 3, 4]})
    # When we split into size‑2 chunks
    chunks = await splitter.split(df, chunk_size=2)

    # Then we get two DataFrames back
    assert isinstance(chunks, list)
    assert all(isinstance(c, pd.DataFrame) for c in chunks)
    assert len(chunks) == 2

    # And each chunk matches the expected slice
    pd.testing.assert_frame_equal(chunks[0], df.iloc[0:2])
    pd.testing.assert_frame_equal(chunks[1], df.iloc[2:4])

    # And no error notifications were sent
    assert splitter.sns_notifier.sent == []


@pytest.mark.asyncio
async def test_split_error(monkeypatch, splitter):
    # Force DataFrame slicing to raise
    monkeypatch.setattr(
        pd.DataFrame, "__getitem__",
        lambda self, key: (_ for _ in ()).throw(ValueError("slice failed")),
        raising=True
    )

    df = pd.DataFrame({"x": [1, 2, 3]})

    # When split() is called, it should propagate the error
    with pytest.raises(ValueError):
        await splitter.split(df, chunk_size=2)

    # And one MessageError should have been published
    sent = splitter.sns_notifier.sent
    assert len(sent) == 1

    msg = sent[0]
    assert isinstance(msg, MessageError)
    assert msg.subject_message == "Error executing Splitter"
    assert "slice failed" in msg.content_message
