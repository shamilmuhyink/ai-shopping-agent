from fastapi import HTTPException, status

class AIException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)

class MainBackendConnectionError(AIException):
    def __init__(self, detail: str = "Could not connect to the main backend API"):
        super().__init__(detail=detail, status_code=status.HTTP_502_BAD_GATEWAY)

class LLMServiceError(AIException):
    def __init__(self, detail: str = "LLM inference service is currently unavailable"):
        super().__init__(detail=detail, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

class GuardrailViolationError(AIException):
    def __init__(self, detail: str = "Input violates safety or context guardrails"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)
