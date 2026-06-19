from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.security import verify_service_token
from app.core.exceptions import AppException
from app.schemas.common import ApiResponse
from app.schemas.conversation import ConversationResponse
from app.services.memory_service import memory_service

router = APIRouter()

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: UUID, _=Depends(verify_service_token)):
    """
    Fetch the full transcript of a conversation.
    Protected by the service token.
    """
    conv = await memory_service.get_conversation_history(conversation_id)
    if not conv:
        raise AppException(
            message="Conversation not found", 
            code="CONVERSATION_NOT_FOUND", 
            status_code=404
        )
    return ApiResponse.success(data=conv).model_dump()
