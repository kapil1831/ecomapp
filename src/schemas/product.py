from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .category import CategoryOut, CategoryBase

class ProductBase(BaseModel):
    title: str
    description: str = "no description"
    price: int
    discount_percentage: float = 0.0
    rating: float = 0.0
    stock: int
    brand: str
    thumbnail: Optional[str] = None
    images: Optional[str] = ""
    is_published: bool = False
    
    
class ProductCreate(ProductBase):
    categories: List[str] = []


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    discount_percentage: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    brand: Optional[str] = None
    thumbnail: Optional[str] = None
    images: Optional[str] = None
    is_published: Optional[bool] = None
    categories: Optional[List[str]] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class ProductsOut(BaseModel):
    message: str
    count: int
    data: List[ProductOut]
    
class ProductUpdateOut(BaseModel):
    message: str
    data: ProductOut | None = None

class ProductWithCategoriesOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryOut] = []
    
    model_config = {"from_attributes": True}

class ProductDeleteOut(ProductUpdateOut):
    pass

class CategoryOutWithProducts(CategoryBase):
    products: List[ProductBase] = []
    
    model_config = {"from_attributes": True}  