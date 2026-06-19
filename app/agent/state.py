from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    State definition for the LangGraph orchestrator.
    """
    # The history of messages in the conversation
    messages: Annotated[List[BaseMessage], operator.add]
    
    # The current active sub-agent (e.g., "order_status", "product_search")
    active_agent: Optional[str]
    
    # Optional context collected by agents
    context: Optional[dict]
    
    # Flag to trigger escalation
    escalate: bool
