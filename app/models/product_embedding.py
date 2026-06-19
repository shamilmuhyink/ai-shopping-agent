import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ProductEmbedding(Base, TimestampMixin):
    __tablename__ = "product_embeddings"

    # We use the main backend's product UUID as the primary key here to maintain 1:1 mapping
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    # Store essential product data to avoid extra API hops during RAG context assembly
    product_data: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Store the vector embedding (e.g., 384 dimensions for bge-small-en-v1.5)
    embedding: Mapped[Vector] = mapped_column(Vector(384), nullable=False)
