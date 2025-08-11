from sqlalchemy.orm import Session
from ..models.models import Category, Product
from sqlalchemy import select, delete, update
from ..schemas.product import ProductOut, ProductCreate,ProductUpdate, ProductsOut, ProductWithCategoriesOut

class ProductService:
    
    @staticmethod
    def get_all_products(session: Session) -> ProductsOut:
        #newer syntax, >=2.0
        stmt = select(Product)
        products = session.execute(stmt).scalars().all()
        
        return {"message": "All Products", "count": len(products), "data": products}
    
    
    @staticmethod
    def get_product(id: int, session: Session) -> ProductWithCategoriesOut:
        # syntax , 2.0
        stmt = select(Product).where(Product.id == id)
        product = session.execute(stmt).scalars().first()
        if product is None:
            return {"message": "product not found for given id"}
        print("adklfnlakjdfjkladjfjkladsklfj:::   ",  product)
        return product
    
    
    @staticmethod
    def update_product(id: int, updated_product: ProductUpdate, session: Session):
        product = session.get(Product, id)
        
        if product is None:
            return {"message": "product not found for given id"}
        
        update_data = updated_product.model_dump(exclude_unset=True, exclude={"categories"})
        for key, value in update_data.items():
            setattr(product, key, value)
            
        product_categories = updated_product.categories
        
        #[TODO] need to fix this, it can fail with exceptions
        if product_categories:
            updated_categories = []
            for category_name in product_categories:
                existing_category = session.execute(select(Category).
                                        where(Category.name == category_name)
                                        ).scalar_one_or_none()
                
                if existing_category:
                    updated_categories.append(existing_category)
                    continue
                
                # it can fail with exceptions, so need to fix it
                new_category = Category(name=category_name)
                session.add(new_category)
                updated_categories.append(new_category)
                
            product.categories = updated_categories  # remove duplicates if any
        
        session.commit()
        session.refresh(product)
        
        return {"message": "successfully updated the product", "data": product}
        
    
    
    @staticmethod
    def create_product(product_payload: ProductCreate, session: Session):
        #old syntax
        product = Product(**product_payload.model_dump(exclude={"categories"}))
        product_categories = product_payload.categories
        
        if product_categories:
            for category_name in product_categories:
                existing_category = session.execute(select(Category).
                                        where(Category.name == category_name)
                                        ).scalar_one_or_none()
                
                if existing_category:
                    product.categories.append(existing_category)
                else:
                    # it can fail with exceptions, so need to fix it
                    new_category = Category(name=category_name)
                    session.add(new_category)
                    product.categories.append(new_category)
        
        session.add(product)
        session.commit()
        session.refresh(product)
        
        return product
    
    
    @staticmethod
    def remove_product(id: int, session: Session):
        # new syntax
        stmt = select(Product).where(Product.id == id)
        product = session.execute(stmt).scalars().first()
        
        if product is None:
            return {"message": "product not found"}
        
        del_stmt = delete(Product).where(Product.id == id)
        stmt = session.execute(del_stmt)
        session.commit()
        return {"message": "successfully deleted the product", "data": product}