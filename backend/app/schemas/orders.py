from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: str
    quantity: int
    image: Optional[str] = None

class OrderSchema(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_amount: str
    shipping_address: dict
    payment_status: str = Field(default="Pending")
    order_status: str = Field(default="Processing")
    tracking_id: Optional[str] = None
    tracking_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total_amount: str
    shipping_address: dict

class OrderResponse(OrderSchema):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
