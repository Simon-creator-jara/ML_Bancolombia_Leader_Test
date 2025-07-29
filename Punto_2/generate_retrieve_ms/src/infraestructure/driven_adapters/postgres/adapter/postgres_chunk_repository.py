import psycopg2.pool as pool_py
from psycopg2.extras import execute_values
from typing import List
from src.domain.model.database.gateway.database_gateway import ChunkRepository


class PostgresChunkRepository(ChunkRepository):
    def __init__(self, conn_pool: pool_py.SimpleConnectionPool, table: str = "simon_leader_yes2"):
        self.pool = conn_pool
        self.table = table

    def insert_chunks(self, records: List[float], top_k=3) -> None:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT movie_title, movie_plot, movie_image, chunk_text,
                        embeddings_normalization <#> %s::vector AS distance  -- cosine distance
                    FROM {self.table}
                    ORDER BY embeddings_normalization <#> %s::vector
                    LIMIT %s
                """, (records, records, top_k))
                return cur.fetchall()
        finally:
            self.pool.putconn(conn)
