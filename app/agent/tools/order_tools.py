from uuid import UUID
from langchain_core.tools import tool
from app.clients.main_backend_client import main_backend_client
from app.core.exceptions import MainBackendConnectionError

@tool
async def get_order_status(order_id: str) -> str:
    """
    Fetch the status, total amount, tracking number, and items of a customer's order.
    Always ask the customer for their Order ID before calling this tool.
    The order_id must be a valid UUID.
    """
    try:
        uuid_obj = UUID(order_id)
    except ValueError:
        return "Error: Invalid Order ID format. Please provide a valid UUID."
        
    try:
        order_status = await main_backend_client.get_order_status(uuid_obj)
        if not order_status:
            return f"No order found with ID {order_id}."
            
        # Format the response for the LLM
        response = f"Order Status: {order_status.status}\n"
        response += f"Total Amount: ${order_status.total_amount}\n"
        if order_status.tracking_number:
            response += f"Tracking Number: {order_status.tracking_number}\n"
        if order_status.expected_delivery:
            response += f"Expected Delivery: {order_status.expected_delivery}\n"
            
        response += "Items:\n"
        for item in order_status.items:
            response += f"- {item.product_name} (x{item.quantity}) - ${item.price}\n"
            
        return response
    except MainBackendConnectionError as e:
        return f"Error retrieving order: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
