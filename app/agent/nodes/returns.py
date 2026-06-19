from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

from app.agent.prompts.system import RETURNS_AGENT_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools.return_tools import check_return_eligibility
from app.clients.groq_client import get_chat_model


async def returns_node(state: AgentState) -> dict:
    """
    Sub-agent that handles return eligibility checking.
    """
    model = get_chat_model(temperature=0.1)
    tools = [check_return_eligibility]

    agent = create_react_agent(model, tools, prompt=RETURNS_AGENT_SYSTEM_PROMPT)
    result = await agent.ainvoke({"messages": state["messages"]})

    new_messages = result["messages"][len(state["messages"]) :]
    return {"messages": new_messages}
