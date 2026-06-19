# This would typically use langchain_huggingface.HuggingFaceEmbeddings
# but for the skeleton, we define a dummy interface.

class EmbeddingClient:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        # self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    async def embed_query(self, query: str) -> list[float]:
        """
        Embed a single search query.
        Returns a mock vector for skeleton purposes.
        """
        # return await self.embeddings.aembed_query(query)
        return [0.0] * 384  # Mock 384-dimensional vector

embedding_client = EmbeddingClient()
