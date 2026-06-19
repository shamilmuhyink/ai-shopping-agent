from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[UUID] = None

class ChatEventResponse(BaseModel):
    event_type: str = Field(..., description="E.g., 'token', 'tool_start', 'tool_end', 'error'")
    data: Dict[str, Any] = Field(..., description="Payload associated with the event")
    conversation_id: UUID
