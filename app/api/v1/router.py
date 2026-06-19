from fastapi import APIRouter

from app.api.v1.endpoints import chat, conversations, health

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
