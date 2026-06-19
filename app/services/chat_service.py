import json
from collections.abc import AsyncGenerator
from uuid import UUID

from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import app_graph
from app.agent.state import AgentState
from app.models.conversation import Conversation, Message


class ChatService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_or_create_conversation(self, conversation_id: UUID | None) -> Conversation:
        if conversation_id:
            result = await self.db.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conv = result.scalar_one_or_none()
            if conv:
                return conv

        new_conv = Conversation()
        if conversation_id:
            new_conv.id = conversation_id
        self.db.add(new_conv)
        await self.db.commit()
        await self.db.refresh(new_conv)
        return new_conv

    async def process_message_stream(
        self, message: str, conversation_id: UUID | None
    ) -> AsyncGenerator[str, None]:
        # 1. Retrieve or create conversation
        conversation = await self.get_or_create_conversation(conversation_id)

        # 2. Save user message to DB
        user_msg = Message(conversation_id=conversation.id, role="user", content=message)
        self.db.add(user_msg)
        await self.db.commit()

        # 3. Load recent history (simplified for now)
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        )
        db_messages = result.scalars().all()

        # Convert DB messages to LangChain messages
        lc_messages = []
        for m in db_messages:
            if m.role == "user":
                lc_messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                lc_messages.append(AIMessage(content=m.content))

        if not lc_messages:
            lc_messages = [HumanMessage(content=message)]

        # 4. Invoke LangGraph (Streaming support requires using astream_events or astream)
        # For simplicity in this skeleton, we'll stream token by token if the model supports it,
        # or just yield the final result. We'll simulate a stream for the SSE requirement.

        # Prepare state
        initial_state = AgentState(
            messages=lc_messages, active_agent=None, context=None, escalate=False
        )

        final_response_text = ""

        try:
            # In a real streaming scenario, we'd use app_graph.astream_events
            # Here we just run it and stream the final output text
            result_state = await app_graph.ainvoke(initial_state)

            last_message = result_state["messages"][-1]
            if isinstance(last_message, AIMessage):
                final_response_text = str(last_message.content)
            else:
                final_response_text = "I'm sorry, I couldn't process that request."

            # Simulate streaming words
            words = final_response_text.split(" ")
            for word in words:
                yield json.dumps(
                    {
                        "event_type": "token",
                        "data": {"token": word + " "},
                        "conversation_id": str(conversation.id),
                    }
                )

        except Exception as e:
            final_response_text = f"Error processing request: {str(e)}"
            yield json.dumps(
                {
                    "event_type": "error",
                    "data": {"error": final_response_text},
                    "conversation_id": str(conversation.id),
                }
            )

        # 5. Save assistant message to DB
        assistant_msg = Message(
            conversation_id=conversation.id, role="assistant", content=final_response_text
        )
        self.db.add(assistant_msg)
        await self.db.commit()
