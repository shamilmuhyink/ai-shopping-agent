from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.v1.router import api_router
from app.clients.main_backend_client import main_backend_client
from app.core.config import get_settings
from app.core.exceptions import AppException
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


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    from app.schemas.common import ApiError, ApiResponse

    correlation_id = getattr(request.state, "correlation_id", "unknown")
    errors = [ApiError(code=exc.code, field=None, message=exc.message)]
    if exc.details:
        for field, msg in exc.details.items():
            errors.append(ApiError(code=exc.code, field=str(field), message=str(msg)))

    response = ApiResponse.error(message=exc.message, errors=errors)
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
        headers={"X-Request-ID": correlation_id},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    from app.schemas.common import ApiError, ApiResponse

    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.exception(
        "unhandled_exception",
        exc_info=exc,
        request_id=correlation_id,
        path=request.url.path,
    )
    response = ApiResponse.error(
        message="An unexpected error occurred. Our team has been notified.",
        errors=[ApiError(code="INTERNAL_SERVER_ERROR", field=None, message=str(exc))],
    )
    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
        headers={"X-Request-ID": correlation_id},
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["health"])
async def health_check() -> dict:
    from app.schemas.common import ApiResponse
    response = ApiResponse.success(
        data={"status": "ok", "service": "ai-assistant"},
        message="Service is healthy",
    )
    return response.model_dump()
