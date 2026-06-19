from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_embedding import ProductEmbedding

class EmbeddingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_similar_products(self, query_embedding: list[float], limit: int = 5) -> List[ProductEmbedding]:
        """
        Search for similar products using pgvector's cosine distance.
        """
        result = await self.session.execute(
            select(ProductEmbedding)
            .order_by(ProductEmbedding.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def upsert_product_embedding(self, product_id: UUID, product_data: dict, embedding: list[float]) -> ProductEmbedding:
        """
        Upsert a product embedding (useful for syncing catalogue updates).
        """
        result = await self.session.execute(
            select(ProductEmbedding).where(ProductEmbedding.product_id == product_id)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.product_data = product_data
            existing.embedding = embedding
            product_embedding = existing
        else:
            product_embedding = ProductEmbedding(
                product_id=product_id,
                product_data=product_data,
                embedding=embedding
            )
            self.session.add(product_embedding)
            
        await self.session.commit()
        await self.session.refresh(product_embedding)
        return product_embedding
