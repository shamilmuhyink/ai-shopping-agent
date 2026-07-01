"""Celery task that receives cross-service product embedding requests."""

import asyncio
from uuid import UUID

import structlog
from celery import Task

from app.services.embedding_service import embedding_service
from app.workers.celery_app import celery_app

logger = structlog.get_logger(__name__)

# Maintain a single event loop for this worker process
_loop = None

def _get_loop() -> asyncio.AbstractEventLoop:
    global _loop
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop


@celery_app.task(name="sync_product_embedding_task", bind=True, max_retries=3)
def sync_product_embedding_task(
    self: Task,
    product_id: str,
    product_data: dict,
) -> dict:
    """Sync a product's vector embedding to pgvector.

    This task is dispatched cross-service from the main backend via
    ``send_task``.  It converts the string product_id back to a UUID
    and delegates to ``EmbeddingService.sync_product_embedding``.

    Args:
        product_id: Stringified UUID of the product.
        product_data: Dict with product fields (``name``, ``description``,
            ``sku``, ``price``, ``category_name``).

    Returns:
        Status dict with ``product_id`` on success.

    Raises:
        self.retry: On transient failures (API timeout, DB lock),
            retried up to 3 times with exponential backoff.
    """
    try:
        logger.info(
            "sync_product_embedding_started",
            product_id=product_id,
        )

        pid = UUID(product_id)
        _get_loop().run_until_complete(embedding_service.sync_product_embedding(pid, product_data))

        logger.info(
            "sync_product_embedding_completed",
            product_id=product_id,
        )
        return {"status": "success", "product_id": product_id}

    except Exception as exc:
        logger.error(
            "sync_product_embedding_failed",
            product_id=product_id,
            error=str(exc),
            retry_count=self.request.retries,
        )
        raise self.retry(
            exc=exc,
            countdown=10 * (2 ** self.request.retries),
        ) from exc
