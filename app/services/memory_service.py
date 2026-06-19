from uuid import UUID
from app.core.database import AsyncSessionLocal
from app.repositories.conversation_repo import ConversationRepository

class MemoryService:
    @staticmethod
    async def save_message_to_db(conversation_id: UUID, role: str, content: str, additional_kwargs: dict = None):
        """
        Saves a single message to long-term memory (PostgreSQL).
        """
        async with AsyncSessionLocal() as session:
            repo = ConversationRepository(session)
            await repo.add_message(conversation_id, role, content, additional_kwargs)
            
    @staticmethod
    async def get_conversation_history(conversation_id: UUID):
        """
        Fetches full conversation history from DB.
        """
        async with AsyncSessionLocal() as session:
            repo = ConversationRepository(session)
            return await repo.get_conversation(conversation_id)

memory_service = MemoryService()
