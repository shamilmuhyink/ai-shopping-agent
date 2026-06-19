from langchain_core.messages import AIMessage
from langgraph.graph import END, StateGraph

from app.agent.nodes.escalation import escalation_node
from app.agent.nodes.order_status import order_agent_node
from app.agent.nodes.product_search import product_search_node
from app.agent.nodes.recommendation import recommendation_node
from app.agent.nodes.response_formatter import response_formatter_node
from app.agent.nodes.returns import returns_node
from app.agent.nodes.router import route_message
from app.agent.prompts.system import GENERAL_AGENT_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.clients.groq_client import get_chat_model


async def general_agent_node(state: AgentState) -> dict:
    model = get_chat_model()
    from langchain_core.messages import SystemMessage

    messages = [SystemMessage(content=GENERAL_AGENT_SYSTEM_PROMPT)] + state["messages"]
    response = await model.ainvoke(messages)
    return {"messages": [response]}


def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node("router", route_message)
    workflow.add_node("order_status", order_agent_node)
    workflow.add_node("product_search", product_search_node)
    workflow.add_node("returns", returns_node)
    workflow.add_node("recommendation", recommendation_node)
    workflow.add_node("escalation", escalation_node)
    workflow.add_node("general", general_agent_node)
    workflow.add_node("response_formatter", response_formatter_node)

    # Simple conditional edge based on active_agent
    workflow.add_conditional_edges(
        "router",
        lambda state: state["active_agent"],
        {
            "order_status": "order_status",
            "product_search": "product_search",
            "returns": "returns",
            "recommendation": "recommendation",
            "escalation": "escalation",
            "general": "general",
        },
    )

    # All specialized agents flow into the response formatter
    for node in [
        "order_status",
        "product_search",
        "returns",
        "recommendation",
        "escalation",
        "general",
    ]:
        workflow.add_edge(node, "response_formatter")

    workflow.add_edge("response_formatter", END)

    workflow.set_entry_point("router")

    return workflow.compile()


app_graph = build_graph()
