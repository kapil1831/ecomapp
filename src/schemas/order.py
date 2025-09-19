from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.models import PaymentStatus, PaymentType

class OrderBase(BaseModel):
    cart_id: int
    user_id: int
    order_details: Optional[dict] = {}
    order_items: Optional[list[dict]] = []
    address: str
    
class OrderCreate(OrderBase):
    payment_status: Optional[str] = PaymentStatus.PENDING
    payment_type: Optional[str] = PaymentType.COD
    payment_details: Optional[dict] = {}
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    address: Optional[str] = None
    payment_status: Optional[str] = None
    payment_type: Optional[str] = None
    payment_details: Optional[dict] = None

class OrderOut(OrderBase):
    id: int
    payment_status: str
    payment_type: str
    payment_details: dict
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