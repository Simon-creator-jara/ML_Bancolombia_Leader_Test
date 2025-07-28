import pytest
from pydantic import ValidationError
from src.domain.model.dataset.dataset_model import RawDataset


def test_rawdataset_accepts_valid_file_path():
    ds = RawDataset(file_path="path/to/file.csv")
    assert ds.file_path == "path/to/file.csv"


def test_rawdataset_requires_file_path():
    with pytest.raises(ValidationError):
        RawDataset()
