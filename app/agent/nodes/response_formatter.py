from app.agent.state import AgentState

async def response_formatter_node(state: AgentState) -> dict:
    """
    Optional node to format the final response before sending it to the user.
    Currently acts as a pass-through but can be used for final styling or 
    markdown normalization.
    """
    # For now, it just returns the state as-is
    return state
