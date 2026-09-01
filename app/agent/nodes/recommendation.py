from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent

from app.agent.prompts.system import RECOMMENDATION_AGENT_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools.product_tools import search_products
from app.clients.groq_client import get_chat_model


async def recommendation_node(state: AgentState, config: RunnableConfig) -> dict:
    """
    Sub-agent that provides contextual product recommendations.
    """
    model = get_chat_model(temperature=0.0)
    tools = [search_products]

    # We use LangGraph's prebuilt react agent for tool calling
    agent = create_react_agent(model, tools, prompt=RECOMMENDATION_AGENT_SYSTEM_PROMPT)

    # Run the agent in stream mode to trigger chat model stream events
    final_result = None
    async for chunk in agent.astream({"messages": state["messages"]}, config):
        final_result = chunk

    # Extract new messages from the final result
    new_messages = []
    if final_result and "messages" in final_result:
        new_messages = final_result["messages"][len(state["messages"]):]

    return {"messages": new_messages}
