from typing import Any, Dict, Optional
from uuid import UUID

from app.clients.base import BaseHttpClient
from app.core.config import get_settings
from app.schemas.internal import OrderStatusResponse
from app.core.exceptions import MainBackendConnectionError

settings = get_settings()

class MainBackendClient(BaseHttpClient):
    def __init__(self):
        super().__init__(
            base_url=str(settings.MAIN_BACKEND_URL),
            default_headers={"X-Service-Token": settings.SERVICE_TOKEN, "Accept": "application/json"}
        )

    async def get_order_status(self, order_id: UUID) -> Optional[OrderStatusResponse]:
        """Fetch order status from main backend"""
        try:
            response = await self.get(f"/orders/{order_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            if data.get("success") and "data" in data:
                return OrderStatusResponse(**data["data"])
            return None
        except Exception as e:
            # Depending on how strict we want to be, we could raise or return None
            # Here we'll raise an AIException to be handled by the LangGraph tool layer
            raise MainBackendConnectionError(f"Failed to fetch order status: {str(e)}")

main_backend_client = MainBackendClient()
