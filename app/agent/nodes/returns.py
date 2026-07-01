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

    # Run the agent in stream mode to trigger chat model stream events
    final_result = None
    async for chunk in agent.astream({"messages": state["messages"]}):
        final_result = chunk

    # Extract new messages from the final result
    new_messages = []
    if final_result and "messages" in final_result:
        new_messages = final_result["messages"][len(state["messages"]):]

    return {"messages": new_messages}
