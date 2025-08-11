
from fastapi import HTTPException
from ..schemas.cart import CartDeleteOut, CartUpdate, CartCreate, CartUpdateOut, CartsOut, CartOut, CartWithCartItemsOut
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from ..models.models import Cart, User
from sqlalchemy import exc

class CartService:
    
    @staticmethod
    def get_all_carts(session: Session) -> CartsOut:
        carts = session.execute(select(Cart)).scalars().all()
        return {"message": "all existing carts", "count":len(carts), "data":carts}
    
    
    @staticmethod
    def get_cart(id: int, session: Session) -> CartWithCartItemsOut:
        cart = session.execute(select(Cart).where(Cart.id == id)).scalars().first()
        if cart is None:
            raise HTTPException(status_code=404, detail="cart not found for given id")
        return cart
    
    
    @staticmethod
    def update_cart(id: int, cart_payload: CartUpdate, session: Session) -> CartUpdateOut:
        cart = session.get(Cart, id)
        
        if cart is None:
            return CartUpdateOut(message="cart not found for given id", data=None)    

        update_data = cart_payload.model_dump(include={"total_amount"})
        
        for key, value in update_data.items():
            setattr(cart, key, value)
            
        session.commit()
        session.refresh(cart)
        
        return CartUpdateOut(message="successfully updated the cart", data=cart)
    
    #[TODO] user should be current active user
    @staticmethod
    def create_cart(cart_payload: CartCreate, session: Session) -> CartOut:
        #[TODO]
        #handle failure  if creation fails : 1. when same cart created twice
        try:
            user_id = cart_payload.user_id
            user_exists = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
            
            if user_exists is None:
                return {"message": f"User with id {user_id} not found"}
            
            
            cart = Cart(user_id=user_id)
            cart.user = user_exists
            
            session.add(cart)
            session.commit()
            session.refresh(cart)
            return cart 
        except exc.IntegrityError as e:
            print(e)
            raise HTTPException(status_code=400, detail="Unique user for each cart")
    
    @staticmethod
    def remove_cart(id: int, session: Session) -> CartDeleteOut:
        # using old syntax
        cart = session.get(Cart, id)
        
        if cart is None:
            return {"message": "cart not found for given id"}
        
        session.delete(cart)
        session.commit()
        return {"message": "successfully deleted cart with given id", "data":cart}
    
    @staticmethod
    def clear_cart(id: int, session: Session) -> CartDeleteOut:
        cart = session.get(Cart, id)
        
        if cart is None:
            return CartDeleteOut(message="cart not found for given id", data=None)
        
        cart.total_amount = 0
        cart.cart_items.clear()  # Assuming cart_items is a relationship that can be cleared    
        session.commit()
        session.refresh(cart)   
        return CartDeleteOut(message="successfully cleared the cart", data=cart)