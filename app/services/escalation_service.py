import json
from app.core.database import AsyncSessionLocal
from app.repositories.conversation_repo import ConversationRepository

class EscalationService:
    @staticmethod
    async def trigger_escalation(conversation_id: str, reason: str = "AI unconfident or explicit request"):
        """
        Creates an escalation record and flags the conversation.
        """
        # We would create an Escalation record here.
        # For now, we update the conversation status to 'escalated'
        async with AsyncSessionLocal() as session:
            repo = ConversationRepository(session)
            conv = await repo.get_conversation(conversation_id)
            if conv:
                conv.status = "escalated"
                await session.commit()
                # In a real system, this would trigger an SQS/RabbitMQ event or an email to support

escalation_service = EscalationService()
