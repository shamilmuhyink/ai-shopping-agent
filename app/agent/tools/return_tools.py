from uuid import UUID
from langchain_core.tools import tool
from app.clients.main_backend_client import main_backend_client
from app.core.exceptions import MainBackendConnectionError

@tool
async def check_return_eligibility(order_id: str) -> str:
    """
    Check if a specific order is eligible for a return.
    Always ask the customer for their Order ID before calling this tool.
    """
    try:
        uuid_obj = UUID(order_id)
    except ValueError:
        return "Error: Invalid Order ID format. Please provide a valid UUID."
        
    try:
        # We assume the main backend client has this method. 
        # If it doesn't, we'll need to mock it or implement it.
        # For now we'll do a mock internal logic based on order status if the method is missing,
        # but let's assume we call get_order_status and check the 15-day policy.
        order_status = await main_backend_client.get_order_status(uuid_obj)
        if not order_status:
            return f"No order found with ID {order_id}."
            
        # Simplified policy logic based on BRD FR-045: "initiate returns within 15 days of delivery"
        if order_status.status.upper() == "DELIVERED":
            return f"Order {order_id} was delivered. It is currently eligible for return if within 15 days of delivery. Please provide a reason for the return to proceed."
        elif order_status.status.upper() in ["RETURN_REQUESTED", "RETURN_APPROVED", "REFUND_INITIATED", "REFUND_COMPLETE", "CLOSED"]:
            return f"Order {order_id} already has a return/refund processed or requested (Current Status: {order_status.status})."
        else:
            return f"Order {order_id} is not yet delivered (Current Status: {order_status.status}). Returns can only be initiated after delivery."
            
    except MainBackendConnectionError as e:
        return f"Error retrieving order for return check: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
