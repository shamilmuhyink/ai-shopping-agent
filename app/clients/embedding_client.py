from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingClient:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"}
        )

    async def embed_query(self, query: str) -> list[float]:
        """
        Embed a single search query.
        """
        return await self.embeddings.aembed_query(query)

embedding_client = EmbeddingClient()
