from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from app.agent.prompts.system import ORDER_AGENT_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools.order_tools import get_order_status
from app.clients.groq_client import get_chat_model


async def order_agent_node(state: AgentState) -> dict:
    """
    Sub-agent that handles order status inquiries.
    """
    model = get_chat_model(temperature=0.1)
    tools = [get_order_status]

    # We use LangGraph's prebuilt react agent for tool calling
    agent = create_react_agent(model, tools, prompt=ORDER_AGENT_SYSTEM_PROMPT)

    # Run the agent with the current messages
    result = await agent.ainvoke({"messages": state["messages"]})

    # The agent returns the updated list of messages, we only want to append the new ones
    # The last message is the final response
    new_messages = result["messages"][len(state["messages"]) :]

    return {"messages": new_messages}
