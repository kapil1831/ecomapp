from pydantic import BaseModel
from typing import List, Optional, TypeVar, Generic
from datetime import datetime
from ..models.models import PaymentStatus, PaymentType
from pydantic.generics import GenericModel

T = TypeVar('T') 

class ResponseWrapper(GenericModel, Generic[T]):
    message: str
    count: Optional[int] = None
    data: Optional[T] = None

class OrderBase(BaseModel):
    cart_id: int
    user_id: int
    order_details: Optional[dict] = {}
    order_items: Optional[list[dict]] = []
    address: str
    
    class Config:
        from_attributes = True
    
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
    
    class Config:
        from_attributes = True

class OrderOut(OrderBase):
    id: int
    payment_status: str
    payment_type: str
    payment_details: dict
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}