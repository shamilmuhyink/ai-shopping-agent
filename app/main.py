from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.clients.main_backend_client import main_backend_client
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.middleware.correlation_id import CorrelationIdMiddleware
from app.middleware.request_logger import RequestLoggerMiddleware
import structlog

settings = get_settings()
logger = structlog.get_logger(__name__)

configure_logging(settings.APP_ENV)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Setup before starting the app
    logger.info("ai_assistant_starting", env=settings.APP_ENV)
    yield
    # Teardown after app stops
    await main_backend_client.close()
    logger.info("ai_assistant_shutdown_complete")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.1.0",
    description="Standalone Agentic AI Shopping Assistant microservice",
    lifespan=lifespan,
)

# Middleware registration
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(CorrelationIdMiddleware)

# CORS configuration
if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(api_router, prefix="/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "ai-assistant"}
