from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.core.database import get_db
from app.schemas.chat import ChatMessageRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/message")
async def send_message(
    request: ChatMessageRequest, db: AsyncSession = Depends(get_db)
) -> EventSourceResponse:
    """
    Send a message to the AI assistant and stream the response via Server-Sent Events (SSE).
    Time to First Token (TTFT) should be < 1.5s as per BRD.
    """
    chat_service = ChatService(db)

    # We return an EventSourceResponse which streams the generator
    return EventSourceResponse(
        chat_service.process_message_stream(request.message, request.conversation_id)
    )
