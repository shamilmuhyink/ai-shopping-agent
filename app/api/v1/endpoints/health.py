from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    """
    Health check endpoint for ECS/EKS to verify the AI assistant service is alive.
    """
    return {"status": "ok", "service": "Agentic AI Shopping Assistant v1.1"}
