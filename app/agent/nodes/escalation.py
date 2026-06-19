from langchain_core.messages import AIMessage
from app.agent.state import AgentState

async def escalation_node(state: AgentState) -> dict:
    """
    Handles escalation to a human support agent.
    Mutates the state to flag for escalation.
    """
    msg = AIMessage(content="I am unable to confidently assist with this request. I am escalating this conversation to a human support agent. Please hold on.")
    return {"messages": [msg], "escalate": True}
