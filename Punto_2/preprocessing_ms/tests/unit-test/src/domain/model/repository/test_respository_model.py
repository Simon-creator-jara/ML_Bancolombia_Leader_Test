from pydantic import ValidationError
import pytest
from src.domain.model.repository.repository_model import GetJson, SaveJson


def test_get_json_model():
    """Test valid initialization of the GetJson model with correct S3 path."""
    get_json = GetJson(s3_path="s3://bucket/file.json")
    assert get_json.s3_path == "s3://bucket/file.json"
    assert get_json.s3_path.startswith("s3://")


def test_get_json_model_error():
    """Test that GetJson raises ValidationError when given an invalid S3 path
    type."""
    with pytest.raises(ValidationError):
        GetJson(s3_path=123)


def test_save_json_model():
    """Test valid initialization of the SaveJson model with all required
    fields."""
    save_json = SaveJson(
        bucket="bucket",
        key="output/file.json",
        data={"key": "value"}
    )
    assert save_json.bucket == "bucket"
    assert save_json.key == "output/file.json"
    assert save_json.data == {"key": "value"}


def test_save_json_model_error():
    """Test that SaveJson raises ValidationError when given invalid data
    type."""
    with pytest.raises(ValidationError):
        SaveJson(bucket="bucket", key="output/file.json", data="key")
