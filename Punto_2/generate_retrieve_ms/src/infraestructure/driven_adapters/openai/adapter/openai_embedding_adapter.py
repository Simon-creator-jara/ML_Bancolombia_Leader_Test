from typing import List
from openai import OpenAI
from src.domain.model.embeddings.gateway.embeddings_gateway import EmbeddingGateway


class OpenAIEmbeddingAdapter(EmbeddingGateway):
    """Adapter to call OpenAI embeddings endpoint."""

    def __init__(self, client: OpenAI):
        self.client = client

    def embed_texts(self, texts):
        question=texts.model_dump(exclude_none=True)
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=question["question"]
        )
        return response.data[0].embedding
