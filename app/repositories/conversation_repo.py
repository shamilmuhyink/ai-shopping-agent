from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation, Message
from app.models.tool_call import AgentToolCall

class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: Optional[UUID] = None, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        result = await self.session.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def add_message(self, conversation_id: UUID, role: str, content: str, additional_kwargs: dict = None) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            additional_kwargs=additional_kwargs or {}
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def log_tool_call(self, conversation_id: UUID, tool_name: str, arguments: dict, result: dict = None, status: str = "success", error_message: str = None) -> AgentToolCall:
        tool_call = AgentToolCall(
            conversation_id=conversation_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            status=status,
            error_message=error_message
        )
        self.session.add(tool_call)
        await self.session.commit()
        await self.session.refresh(tool_call)
        return tool_call
