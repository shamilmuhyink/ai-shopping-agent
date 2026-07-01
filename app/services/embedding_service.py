"""Product embedding service — generates and persists vector embeddings."""

from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.embedding_client import embedding_client
from app.core.database import AsyncSessionLocal
from app.repositories.embedding_repo import EmbeddingRepository

logger = structlog.get_logger(__name__)


class EmbeddingService:
    """Generates vector embeddings for products and upserts them to pgvector.

    Called by the ``sync_product_embedding_task`` Celery task, which is
    dispatched cross-service from the main backend whenever a product
    is created, updated, or approved.
    """

    @staticmethod
    def _build_embedding_text(product_data: dict) -> str:
        """Assemble a rich text representation of the product for embedding.

        Combines all available product fields into a single string that
        captures the product's identity for semantic search.  More fields
        produce a richer vector representation.

        Args:
            product_data: Dict with keys like ``name``, ``description``,
                ``sku``, ``price``, ``category_name``.

        Returns:
            A single string optimised for the embedding model.
        """
        parts: list[str] = []

        if name := product_data.get("name"):
            parts.append(name)

        if category := product_data.get("category_name"):
            parts.append(f"Category: {category}")

        if description := product_data.get("description"):
            parts.append(description)

        if sku := product_data.get("sku"):
            parts.append(f"SKU: {sku}")

        if price := product_data.get("price"):
            parts.append(f"Price: ₹{price}")

        return " | ".join(parts)

    @staticmethod
    async def sync_product_embedding(
        product_id: UUID,
        product_data: dict,
    ) -> None:
        """Generate an embedding for a product and upsert it to pgvector.

        This method is the primary entry point called by the Celery task.
        It builds the embedding text, calls the embedding model, and
        persists the result.

        Args:
            product_id: UUID of the product (from the main backend).
            product_data: Dict containing product fields for embedding.

        Raises:
            Exception: Propagated to the Celery task for retry handling.
        """
        text_to_embed = EmbeddingService._build_embedding_text(product_data)

        logger.info(
            "generating_product_embedding",
            product_id=str(product_id),
            text_length=len(text_to_embed),
        )

        vector = await embedding_client.embed_query(text_to_embed)

        async with AsyncSessionLocal() as session:
            repo = EmbeddingRepository(session)
            await repo.upsert_product_embedding(product_id, product_data, vector)
            await session.commit()

        logger.info(
            "product_embedding_synced",
            product_id=str(product_id),
            vector_dimensions=len(vector),
        )


embedding_service = EmbeddingService()
