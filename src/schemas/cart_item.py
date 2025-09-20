from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    product_price: int
    quantity: int = 1    
    
class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemOut(CartItemBase):
    id: int
    subtotal: float = 0.0
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class CartItemsOut(BaseModel):
    message: str
    count: int
    data: List[CartItemOut]
    
class CartItemUpdateOut(BaseModel):
    message: str
    data: CartItemOut | None = None

class CartItemDeleteOut(CartItemUpdateOut):
    pass