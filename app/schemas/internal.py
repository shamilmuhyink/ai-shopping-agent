from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

# Schemas representing data fetched from the main backend

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    price: Decimal

class OrderStatusResponse(BaseModel):
    order_id: UUID
    status: str
    total_amount: Decimal
    items: List[OrderItem]
    tracking_number: Optional[str] = None
    expected_delivery: Optional[str] = None

class ProductCatalogResponse(BaseModel):
    product_id: UUID
    name: str
    description: str
    price: Decimal
    stock: int
    status: str
