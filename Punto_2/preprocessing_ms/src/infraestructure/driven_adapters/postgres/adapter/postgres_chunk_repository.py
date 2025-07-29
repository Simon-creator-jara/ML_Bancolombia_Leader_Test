import psycopg2.pool as pool_py
from psycopg2.extras import execute_values
from typing import List, Tuple
from src.domain.model.database.gateway.database_gateway import ChunkRepository


class PostgresChunkRepository(ChunkRepository):
    def __init__(self, conn_pool: pool_py.SimpleConnectionPool, table: str = "simon_leader_yes2"):
        self.pool = conn_pool
        self.table = table

    def insert_chunks(self, records: List[Tuple]) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                sql = f"""
                    INSERT INTO {self.table}
                    (movie_title, chunk_id, chunk_text, movie_plot, movie_image, embedding, embeddings_normalization)
                    VALUES %s
                """
                execute_values(cur, sql, records)
                conn.commit()
                return
        finally:
            self.pool.putconn(conn)
