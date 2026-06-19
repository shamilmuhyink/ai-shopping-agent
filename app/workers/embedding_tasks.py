import asyncio
from uuid import UUID

from celery import Task

from app.services.embedding_service import embedding_service
from app.workers.celery_app import celery_app


@celery_app.task(name="sync_product_embedding_task", bind=True, max_retries=3)
def sync_product_embedding_task(self: Task, product_id: str, product_data: dict) -> dict:
    """
    Celery task to sync product embeddings.
    Since sync_product_embedding is an async method, we wrap it with asyncio.run.
    """
    try:
        pid = UUID(product_id)
        asyncio.run(embedding_service.sync_product_embedding(pid, product_data))
        return {"status": "success", "product_id": product_id}
    except Exception as exc:
        # Retry in 10 seconds if there's an API failure or DB lock
        raise self.retry(exc=exc, countdown=10) from exc
