import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.infraestructure.helpers.utils import load_json_file


class TestUtils:
    """Test suite for utility functions in the helpers module."""

    def test_load_json_file_with_string_path(self, tmp_path):
        """Test loading a JSON file with a string path.

        Verifies that load_json_file correctly:
        - Reads a JSON file provided as a string path
        - Returns the parsed JSON data as a Python dictionary
        - Uses cache when the file is no longer available

        Args:
            tmp_path: Pytest fixture providing a temporary directory path.
        """
        test_data = {"key": "value", "number": 42}
        json_file = tmp_path / "test.json"
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(test_data, f)
        result = load_json_file(str(json_file))
        assert result == test_data
        os.remove(json_file)
        cached_result = load_json_file(str(json_file))
        assert cached_result == test_data

    def test_load_json_file_with_path_object(self, tmp_path):
        """Test loading a JSON file with a Path object.

        Verifies that load_json_file correctly handles Path objects as input
        and returns the expected parsed JSON data.

        Args:
            tmp_path: Pytest fixture providing a temporary directory path.
        """
        test_data = {"key": "value", "nested": {"inner": "data"}}
        json_file = tmp_path / "test_path.json"
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(test_data, f)
        result = load_json_file(json_file)
        assert result == test_data

    def test_load_json_file_with_complex_data(self, tmp_path):
        """Test loading a JSON file with complex data types.

        Verifies that load_json_file correctly handles and preserves various
        data types including:
        - Strings, numbers, floats, booleans, null values
        - Arrays and nested objects

        Args:
            tmp_path: Pytest fixture providing a temporary directory path.
        """
        test_data = {
            "string": "hello",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "nested": {
                "inner": "value",
                "list": ["a", "b", "c"]
            }
        }
        json_file = tmp_path / "complex.json"
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(test_data, f)
        result = load_json_file(json_file)
        assert result == test_data

    def test_load_json_file_file_not_found(self):
        """Test loading a non-existent JSON file raises FileNotFoundError.

        Verifies that load_json_file correctly:
        - Raises a FileNotFoundError when the file doesn't exist
        - Includes the file path in the error message
        """
        non_existent_file = "non_existent_file.json"
        if os.path.exists(non_existent_file):
            os.remove(non_existent_file)
        with pytest.raises(FileNotFoundError) as exc_info:
            load_json_file(non_existent_file)
        assert f"File {non_existent_file} not found" in str(exc_info.value)

    def test_load_json_file_invalid_json(self, tmp_path):
        """Test loading an invalid JSON file raises JSONDecodeError.

        Verifies that load_json_file correctly raises a JSONDecodeError
        when the file contains invalid JSON syntax.

        Args:
            tmp_path: Pytest fixture providing a temporary directory path.
        """
        invalid_json_file = tmp_path / "invalid.json"
        with open(invalid_json_file, 'w', encoding="utf-8") as f:
            f.write("{ This is not valid JSON }")
        with pytest.raises(json.JSONDecodeError):
            load_json_file(invalid_json_file)

    def test_load_json_file_cache_works(self):
        """Test that the lru_cache is working properly for load_json_file.

        Verifies that load_json_file correctly:
        - Caches results based on the file path
        - Returns cached data without re-reading the file
        - Uses different cache entries for different file paths
        """
        test_data = {"key": "value"}
        with patch('os.path.exists', return_value=True), \
             patch(
                 'builtins.open',
                 mock_open(read_data=json.dumps(test_data))
             ):
            result1 = load_json_file("test_cache.json")
            assert result1 == test_data
            with patch(
                'builtins.open',
                mock_open(read_data=json.dumps({"different": "data"}))
            ):
                result2 = load_json_file("test_cache.json")
                assert result2 == test_data
                result3 = load_json_file("different_path.json")
                assert result3 == {"different": "data"}

    @pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig"])
    def test_load_json_file_with_different_encodings(self, tmp_path, encoding):
        """Test loading JSON files with different encodings.

        Verifies that load_json_file correctly handles files with different
        character encodings, including special characters.

        Args:
            tmp_path: Pytest fixture providing a temporary directory path.
            encoding: The encoding to use for the test file (parametrized).
        """
        test_data = {"key": "value with special chars: áéíóú"}
        json_file = tmp_path / f"test_{encoding}.json"
        with open(json_file, 'w', encoding=encoding) as f:
            json.dump(test_data, f, ensure_ascii=False)
        result = load_json_file(json_file)
        assert result == test_data
