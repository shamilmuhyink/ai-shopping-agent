from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import verify_service_token
from app.schemas.conversation import ConversationResponse
from app.services.memory_service import memory_service

router = APIRouter()

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: UUID, _=Depends(verify_service_token)):
    """
    Fetch the full transcript of a conversation.
    Protected by the service token.
    """
    conv = await memory_service.get_conversation_history(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv
