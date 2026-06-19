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

    agent = create_react_agent(model, tools, state_modifier=RECOMMENDATION_AGENT_SYSTEM_PROMPT)
    result = await agent.ainvoke({"messages": state["messages"]})
    
    new_messages = result["messages"][len(state["messages"]) :]
    return {"messages": new_messages}
