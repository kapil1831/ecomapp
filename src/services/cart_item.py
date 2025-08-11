
from fastapi import HTTPException
from ..schemas.cart_item import CartItemDeleteOut, CartItemUpdate, CartItemCreate, CartItemUpdateOut, CartItemsOut, CartItemOut
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from ..models.models import CartItem, User, Cart, Product
class CartItemService:
    
    @staticmethod
    def get_all_cart_items(session: Session):
        cart_items = session.execute(select(CartItem)).scalars().all()
        return CartItemsOut(message="all existing carts", count = len(cart_items), data=cart_items)
    
    
    @staticmethod
    def get_cart_item(id: int, session: Session):
        cart_item = session.get(CartItem, id)
        
        if cart_item is None:
            return {"message": "cart_item not found for given id"}
    
        return {"message": "cart_item found by given id", "data": cart_item}
    
    
    @staticmethod
    def update_cart_item(id: int, cart_item_payload: CartItemUpdate, session: Session):
        cart_item = session.get(CartItem, id)
        
        if cart_item is None:
            return CartItemUpdateOut(message="No such CartItem exist in your cart", data=None)
        
        product = session.get(Product, cart_item.product_id)
        subtotal = cart_item_payload.quantity*(product.price*(1-(product.discount_percentage/100)))
        
        cart = session.get(Cart, cart_item.cart_id)
        if cart is None:
            return CartItemUpdateOut(message="No such Cart exists", data=None)
        
        cart.total_amount -= cart_item.subtotal  # deduct old subtotal
        cart.total_amount += subtotal  # add new subtotal
        
        update_data = cart_item_payload.model_dump(include={"quantity"})
        update_data.update({"subtotal": subtotal})
        
        for key, value in update_data.items():
            setattr(cart_item, key, value)
            
        session.commit()
        session.refresh(cart_item)
        return CartItemUpdateOut(message="successfully updated the cart item", data=cart_item)
            
        
    
    
    @staticmethod
    def create_cart_item(cart_item_payload: CartItemCreate, session: Session):
        
        cart_id = cart_item_payload.cart_id
        product_id = cart_item_payload.product_id
        
        cart = session.get(Cart, cart_id)
        
        if cart is None:
            raise HTTPException(status_code=404, detail="cart not found for given id")
        
        product = session.get(Product, product_id)        
        
        if product is None:
             raise HTTPException(status_code=404, detail="product not found for given id")
        
        existing_cart_item = session.execute(select(CartItem).filter_by(product_id=product_id, cart_id=cart_id)).scalar()
        
        if existing_cart_item:
            existing_cart_item.quantity += cart_item_payload.quantity
            extra_subtotal = cart_item_payload.quantity*(product.price*(1- (product.discount_percentage/100)))
            existing_cart_item.subtotal += extra_subtotal
            cart.total_amount += extra_subtotal
            session.commit()
            session.refresh(existing_cart_item)
            return existing_cart_item
        
        subtotal = cart_item_payload.quantity*(product.price*(1- (product.discount_percentage/100)))
        cart.total_amount += subtotal  #total amount should be a derived value rather than a stored value
        cart_item = CartItem(**cart_item_payload.model_dump(exclude={"subtotal"}), subtotal=subtotal, product=product, cart=cart)
        
        session.add(cart_item)
        session.commit()
        session.refresh(cart_item)
        
        return cart_item
        
    
    
    @staticmethod
    def remove_cart_item(id: int, session: Session):
        cart_item = session.get(CartItem, id)
        
        if cart_item is None:
            return CartItemDeleteOut(message="cart not found for given id")
        
        cart = session.get(Cart, cart_item.cart_id)
        if cart is None:
            return CartItemDeleteOut(message="No such Cart exists", data=None)
        cart.total_amount -= cart_item.subtotal

        session.delete(cart_item)
        session.commit()
        
        return CartItemDeleteOut(message="successfully deleted cart item with given id", data=cart_item)
        