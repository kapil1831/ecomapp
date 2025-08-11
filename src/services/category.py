
from fastapi import HTTPException
from ..schemas.category import CategoryDeleteOut, CategoryUpdate, CategoryCreate, CategoriesOut, CategoryOut
from ..schemas.product import CategoryOutWithProducts
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from ..models.models import Category

class CategoryService:
    
    @staticmethod
    def get_all_categories( session: Session) -> CategoriesOut:
        cats = session.execute(select(Category)).scalars().all()
        return {"message": "all existing categories", "count":len(cats), "data":cats}
    
    @staticmethod
    def get_category(id: int, session:Session) -> CategoryOutWithProducts:
        category = session.execute(select(Category).where(Category.id == id)).scalars().first()
        print(category)    
        if category is None:
            raise HTTPException(status_code=404, detail="category not found for given id")
        return category
        
    
    @staticmethod
    def update_category(id: int, updated_category: CategoryUpdate, session: Session):
        db_category = session.get(Category, id)
        
        if db_category is None:
            return {"message": "category not found for given id"}
        
        for key, value in updated_category.model_dump().items():
            setattr(db_category, key, value)
        
        session.commit()
        session.refresh(db_category)
        return {"message": "successfully updated the category", "data": db_category}
    
        
    
    
    @staticmethod
    def create_category(category_payload: CategoryCreate, session: Session) -> CategoryOut:
        # using old syntax, <2.0
        
        #[TODO]
        #handle failure  if creation fails : 1. when same category created twice
        category = Category(**category_payload.model_dump())
        session.add(category)
        session.commit()
        session.refresh(category)
        return {"message": "successfully created the category", "data": category}
    
    
    @staticmethod
    def remove_category(id: int, session: Session) -> CategoryDeleteOut:
        # using old syntax
        category = session.get(Category, id)
        
        if category is None:
            return {"message": "category not found for given id"}
        
        session.delete(category)
        session.commit()
        return {"message": "successfully deleted category with given id", "data":category}