import redis.asyncio as redis
from typing import AsyncGenerator

from app.core.config import get_settings

settings = get_settings()

redis_client = redis.from_url(str(settings.REDIS_URL), decode_responses=True)

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    yield redis_client
