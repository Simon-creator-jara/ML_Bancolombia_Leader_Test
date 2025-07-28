import pytest
from unittest.mock import MagicMock, patch
import psycopg2.pool as pool_py
from psycopg2.extras import execute_values
from typing import List, Tuple

from src.infraestructure.driven_adapters.postgres.adapter.postgres_chunk_repository import PostgresChunkRepository


@pytest.fixture
def mock_conn_pool():
    mock_pool = MagicMock(spec=pool_py.SimpleConnectionPool)
    mock_pool.getconn.return_value = MagicMock()
    return mock_pool

@pytest.fixture
def mock_connection(mock_conn_pool):
    return mock_conn_pool.getconn.return_value

@pytest.fixture
def mock_cursor(mock_connection):
    mock_cursor_instance = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor_instance
    return mock_cursor_instance

@pytest.fixture
def repository(mock_conn_pool):
    return PostgresChunkRepository(conn_pool=mock_conn_pool, table="test_chunks")


def test_insert_chunks_success(repository, mock_conn_pool, mock_connection, mock_cursor):
    records_to_insert = [
        ("Movie A", 1, "Chunk 1 text", "Plot A", "Image A", [0.1, 0.2], 0.9),
        ("Movie B", 2, "Chunk 2 text", "Plot B", "Image B", [0.3, 0.4], 0.8),
    ]

    with patch("src.infraestructure.driven_adapters.postgres.adapter.postgres_chunk_repository.execute_values") as mock_execute_values:
        repository.insert_chunks(records_to_insert)

        mock_conn_pool.getconn.assert_called_once()

        mock_connection.cursor.assert_called_once()
        mock_connection.cursor.return_value.__enter__.assert_called_once()
        mock_connection.cursor.return_value.__exit__.assert_called_once()

        expected_sql_prefix = f"INSERT INTO {repository.table}"
        mock_execute_values.assert_called_once()
        assert mock_execute_values.call_args[0][1].strip().startswith(expected_sql_prefix)
        assert mock_execute_values.call_args[0][2] == records_to_insert

        mock_connection.commit.assert_called_once()

        mock_conn_pool.putconn.assert_called_once_with(mock_connection)

def test_insert_chunks_exception_handling(repository, mock_conn_pool, mock_connection, mock_cursor):
    records_to_insert = [
        ("Movie C", 3, "Chunk 3 text", "Plot C", "Image C", [0.5, 0.6], 0.7),
    ]

    mock_exception = Exception("Database error")
    with patch("src.infraestructure.driven_adapters.postgres.adapter.postgres_chunk_repository.execute_values", side_effect=mock_exception):
        with pytest.raises(Exception) as excinfo:
            repository.insert_chunks(records_to_insert)

        assert str(excinfo.value) == "Database error"

        mock_conn_pool.getconn.assert_called_once()

        mock_connection.cursor.assert_called_once()

        mock_connection.commit.assert_not_called()

        mock_conn_pool.putconn.assert_called_once_with(mock_connection)