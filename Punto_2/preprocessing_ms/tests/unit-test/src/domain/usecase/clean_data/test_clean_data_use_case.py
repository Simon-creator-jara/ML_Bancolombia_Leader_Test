# tests/unit/test_dataset_cleaner_impl.py

import pytest
import pandas as pd
from types import SimpleNamespace
from src.domain.usecase.clean_data.clean_data_use_case import DatasetCleanerImpl
from src.domain.model.dataset.dataset_model import RawDataset
from src.domain.model.message_error.message_error_model import MessageError

# A dummy SNS notifier that captures sent messages


class DummySNS:
    def __init__(self):
        self.sent = []

    async def send(self, message_error: MessageError):
        self.sent.append(message_error)


@pytest.fixture
def logger():
    # stub logger
    return SimpleNamespace(info=lambda *args, **kwargs: None,
                           error=lambda *args, **kwargs: None)


@pytest.fixture
def sns_notifier():
    return DummySNS()


@pytest.fixture
def cleaner(logger, sns_notifier):
    return DatasetCleanerImpl(logger=logger, sns_notifier=sns_notifier)


@pytest.mark.asyncio
async def test_process_success(monkeypatch, cleaner):
    # Prepare a DataFrame with dirty title and plot
    df = pd.DataFrame([{
        "title": "Bad 'Title' (remove)",
        "plot": "Plot with email test@example.com and <ref>refs</ref>"
    }])
    # Make pd.read_csv return our dummy DataFrame
    monkeypatch.setattr(pd, "read_csv", lambda path: df.copy())

    raw = RawDataset(file_path="dummy.csv")
    result = await cleaner.process(raw)

    # Should have added text_to_embed
    assert "text_to_embed" in result.columns

    # Title cleaned: no quotes or parentheses
    assert "'" not in result.at[0, "title"]
    assert "(" not in result.at[0, "title"]

    # Plot cleaned: no email or ref tags
    plot = result.at[0, "plot"]
    assert "test@example.com" not in plot
    assert "<ref>" not in plot

    # SNS should not have been invoked
    assert cleaner.sns_notifier.sent == []


@pytest.mark.asyncio
async def test_process_error(monkeypatch, cleaner):
    # Make pd.read_csv raise an error
    monkeypatch.setattr(pd, "read_csv", lambda path: (
        _ for _ in ()).throw(RuntimeError("read failure")))

    raw = RawDataset(file_path="missing.csv")
    with pytest.raises(RuntimeError):
        await cleaner.process(raw)

    # SNS notifier should have been called once
    sent = cleaner.sns_notifier.sent
    assert len(sent) == 1
    msg = sent[0]
    assert isinstance(msg, MessageError)
    assert "Error executing DataCleaner" in msg.subject_message
    assert "read failure" in msg.content_message
