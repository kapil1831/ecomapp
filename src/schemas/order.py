from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderBase(BaseModel):
    id: int
    cart_id: int
    user_id: int
    order_details: dict
    order_items: dict
    address: str
    
class OrderCreate(OrderBase):
    payment_status: Optional[str] = "pending"
    payment_type: Optional[str] = "cash on delivery"
    payment_details: Optional[dict] = dict
    pass

class OrderUpdate(OrderCreate):
    pass

class OrderOut(OrderBase):
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class OrdersOut(BaseModel):
    message: str
    count: int
    data: List[OrderOut]
    
class OrderUpdateOut(BaseModel):
    message: str
    data: OrderOut | None = None

class OrderDeleteOut(OrderUpdateOut):
    pass