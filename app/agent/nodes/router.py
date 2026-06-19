from langchain_core.messages import SystemMessage

from app.agent.prompts.system import ROUTER_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.clients.groq_client import get_chat_model


async def route_message(state: AgentState) -> dict:
    """
    Analyzes the latest message and determines which sub-agent should handle it.
    """
    model = get_chat_model(temperature=0.0)
    messages = [SystemMessage(content=ROUTER_SYSTEM_PROMPT)] + state["messages"][-1:]

    response = await model.ainvoke(messages)
    decision = response.content.strip().lower()

    valid_agents = ["order_status", "product_search", "returns", "general"]
    if decision not in valid_agents:
        decision = "general"

    return {"active_agent": decision}
