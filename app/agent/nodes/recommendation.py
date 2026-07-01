from langgraph.prebuilt import create_react_agent

from app.agent.prompts.system import RECOMMENDATION_AGENT_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools.product_tools import search_products
from app.clients.groq_client import get_chat_model

async def recommendation_node(state: AgentState) -> dict:
    """
    Sub-agent that provides contextual product recommendations.
    """
    model = get_chat_model(temperature=0.4)
    tools = [search_products]

    # Run the agent in stream mode to trigger chat model stream events
    final_result = None
    async for chunk in agent.astream({"messages": state["messages"]}):
        final_result = chunk

    # Extract new messages from the final result
    new_messages = []
    if final_result and "messages" in final_result:
        new_messages = final_result["messages"][len(state["messages"]):]

    return {"messages": new_messages}
