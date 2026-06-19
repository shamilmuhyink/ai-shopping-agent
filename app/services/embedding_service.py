from uuid import UUID
from app.core.database import AsyncSessionLocal
from app.repositories.embedding_repo import EmbeddingRepository
from app.clients.embedding_client import embedding_client

class EmbeddingService:
    @staticmethod
    async def sync_product_embedding(product_id: UUID, product_data: dict):
        """
        Generates an embedding for a product and upserts it to pgvector.
        """
        text_to_embed = f"{product_data.get('name', '')} {product_data.get('description', '')}"
        
        vector = await embedding_client.embed_query(text_to_embed)
        
        async with AsyncSessionLocal() as session:
            repo = EmbeddingRepository(session)
            await repo.upsert_product_embedding(product_id, product_data, vector)

embedding_service = EmbeddingService()
