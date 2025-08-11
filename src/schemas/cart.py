from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .cart_item  import CartItemOut

class CartBase(BaseModel):
    user_id: int
    total_amount: float = 0.0
    grand_total: float = 0.0
    item_count: int = 0
    total_discount: float = 0.0
    
    
class CartCreate(BaseModel):
    user_id: int


class CartUpdate(BaseModel):
    total_amount: float = 0.0

class CartOut(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class CartsOut(BaseModel):
    message: str
    count: int
    data: List[CartOut]
    
class CartUpdateOut(BaseModel):
    message: str
    data: CartOut | None = None

class CartWithCartItemsOut(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    cart_items: List[CartItemOut] = []    
    model_config = {"from_attributes": True}

class CartDeleteOut(CartUpdateOut):
    pass