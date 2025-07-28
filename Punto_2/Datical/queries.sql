CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE simon_leader_yes2 (
    id SERIAL PRIMARY KEY,
    movie_title TEXT,
    chunk_id INTEGER,
    chunk_text TEXT,
	movie_plot TEXT,
	movie_image TEXT,
    embedding VECTOR(3072),
	embeddings_normalization VECTOR(3072)
);