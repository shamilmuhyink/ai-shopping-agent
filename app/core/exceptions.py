from typing import Optional, Dict, Any
from fastapi import status

class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class AIException(AppException):
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(
            message=detail,
            code="AI_ERROR",
            status_code=status_code
        )


class MainBackendConnectionError(AIException):
    def __init__(self, detail: str = "Could not connect to the main backend API"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_502_BAD_GATEWAY
        )


class LLMServiceError(AIException):
    def __init__(self, detail: str = "LLM inference service is currently unavailable"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class GuardrailViolationError(AIException):
    def __init__(self, detail: str = "Input violates safety or context guardrails"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST
        )
