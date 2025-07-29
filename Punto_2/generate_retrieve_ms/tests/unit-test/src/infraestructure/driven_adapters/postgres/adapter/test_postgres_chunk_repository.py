import pytest
from unittest.mock import MagicMock
from src.infraestructure.driven_adapters.postgres.adapter.postgres_chunk_repository import PostgresChunkRepository
from psycopg2 import pool as pool_py


@pytest.fixture
def mock_conn_pool():
    mock_pool = MagicMock(spec=pool_py.SimpleConnectionPool)
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn
    return mock_pool, mock_conn


@pytest.fixture
def mock_cursor():
    return MagicMock()


@pytest.fixture
def postgres_chunk_repository(mock_conn_pool, mock_cursor):
    mock_pool, mock_conn = mock_conn_pool
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.cursor.return_value.__exit__.return_value = None
    return PostgresChunkRepository(conn_pool=mock_pool)


def test_retrieve_similar_chunks_returns_data(postgres_chunk_repository, mock_conn_pool, mock_cursor):
    records_embedding = [0.1, 0.2, 0.3]
    top_k_limit = 3
    table_name = "simon_leader_yes2"

    expected_query = f"""
                    SELECT movie_title, movie_plot, movie_image, chunk_text,
                        embeddings_normalization <#> %s::vector AS distance  -- cosine distance
                    FROM {table_name}
                    ORDER BY embeddings_normalization <#> %s::vector
                    LIMIT %s
                """

    mock_cursor.fetchall.return_value = [("movie1", "plot1", "image1", "chunk1", 0.1),
                                          ("movie2", "plot2", "image2", "chunk2", 0.2)]

    mock_pool, mock_conn = mock_conn_pool

    result = postgres_chunk_repository.insert_chunks(records_embedding, top_k_limit)

    mock_pool.getconn.assert_called_once()
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(expected_query, (records_embedding, records_embedding, top_k_limit))
    mock_cursor.fetchall.assert_called_once()
    mock_pool.putconn.assert_called_once_with(mock_conn)

    assert result == [("movie1", "plot1", "image1", "chunk1", 0.1),
                      ("movie2", "plot2", "image2", "chunk2", 0.2)]


def test_insert_chunks_handles_exception(postgres_chunk_repository, mock_conn_pool, mock_cursor):
    records_embedding = [0.1, 0.2, 0.3]
    top_k_limit = 3

    mock_pool, mock_conn = mock_conn_pool

    mock_cursor.execute.side_effect = Exception("Database error during query")

    with pytest.raises(Exception, match="Database error during query"):
        postgres_chunk_repository.insert_chunks(records_embedding, top_k_limit)

    mock_pool.getconn.assert_called_once()
    mock_pool.putconn.assert_called_once_with(mock_conn)
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_not_called()