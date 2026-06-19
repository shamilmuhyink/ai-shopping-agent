from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

settings = get_settings()

api_key_header = APIKeyHeader(name="X-Service-Token", auto_error=True)


async def verify_service_token(api_key: str = Security(api_key_header)) -> bool:
    """
    Verify that incoming requests to the AI service contain the correct service token.
    This ensures only authorized services (like the main backend) can call internal endpoints.
    """
    if api_key != settings.SERVICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service token",
        )
    return True
