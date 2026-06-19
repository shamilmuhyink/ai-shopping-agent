from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from app.agent.prompts.system import PRODUCT_AGENT_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools.product_tools import search_products
from app.clients.groq_client import get_chat_model

async def product_search_node(state: AgentState) -> dict:
    """
    Sub-agent that handles product discovery and search queries.
    """
    model = get_chat_model(temperature=0.2)
    tools = [search_products]

    agent = create_react_agent(model, tools, state_modifier=PRODUCT_AGENT_SYSTEM_PROMPT)
    result = await agent.ainvoke({"messages": state["messages"]})
    
    new_messages = result["messages"][len(state["messages"]) :]
    return {"messages": new_messages}
