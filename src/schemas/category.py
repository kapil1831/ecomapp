from pydantic import BaseModel
from typing import List


class CategoryBase(BaseModel):
    id: int
    name: str   
    
    model_config = {"from_attributes": True} 


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    message: str
    data: CategoryBase | None = None

# class CategoryOutWithProducts(CategoryBase):
#     products: List["ProductOut"] = []  

class CategoriesOut(BaseModel):
    message: str
    count: int
    data: List[CategoryBase]

class CategoryDelete(BaseModel):
    id: int
    name: str
    
class CategoryDeleteOut(BaseModel):
    message: str
    data: CategoryBase | None = None