
from fastapi import HTTPException
from ..schemas.order import OrderDeleteOut, OrderUpdate, OrderCreate, OrderUpdateOut, OrdersOut, OrderOut
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from ..models.models import Order, Cart, CartItem
from ..models.users import User

class OrderService:
    
    @staticmethod
    def get_all_orders(session: Session):
        orders = session.execute(select(Order)).scalars().all()
        return OrdersOut(message="all existing carts", count = len(orders), data=orders)
    
    
    @staticmethod
    def get_order(id: int, session: Session):
        order = session.get(Order, id)
        
        if order is None:
            return {"message": "order not found for given id"}
    
        return {"message": "order found by given id", "data": order}
    
    
    @staticmethod
    def update_order(id: int, order_payload: OrderUpdate, session: Session):
        order = session.get(Order, id)
        
        if order is None:
            return OrderUpdateOut(message="No such Order exist in your cart", data=None)
        
        product = session.get(Product, order.product_id)
        subtotal = order_payload.quantity*(product.price*(1-(product.discount_percentage/100)))
        
        cart = session.get(Cart, order.cart_id)
        if cart is None:
            return OrderUpdateOut(message="No such Cart exists", data=None)
        
        cart.total_amount -= order.subtotal  # deduct old subtotal
        cart.total_amount += subtotal  # add new subtotal
        
        update_data = order_payload.model_dump(include={"quantity"})
        update_data.update({"subtotal": subtotal})
        
        for key, value in update_data.items():
            setattr(order, key, value)
            
        session.commit()
        session.refresh(order)
        return OrderUpdateOut(message="successfully updated the cart item", data=order)
            
        
    
    
    @staticmethod
    def create_order(order_payload: OrderCreate, session: Session):
        
        cart_id = order_payload.cart_id
        product_id = order_payload.product_id
        
        cart = session.get(Cart, cart_id)
        
        if cart is None:
            raise HTTPException(status_code=404, detail="cart not found for given id")
        
        product = session.get(Product, product_id)        
        
        if product is None:
             raise HTTPException(status_code=404, detail="product not found for given id")
        
        existing_order = session.execute(select(Order).filter_by(product_id=product_id, cart_id=cart_id)).scalar()
        
        if existing_order:
            existing_order.quantity += order_payload.quantity
            extra_subtotal = order_payload.quantity*(product.price*(1- (product.discount_percentage/100)))
            existing_order.subtotal += extra_subtotal
            cart.total_amount += extra_subtotal
            session.commit()
            session.refresh(existing_order)
            return existing_order
        
        subtotal = order_payload.quantity*(product.price*(1- (product.discount_percentage/100)))
        cart.total_amount += subtotal  #total amount should be a derived value rather than a stored value
        order = Order(**order_payload.model_dump(exclude={"subtotal"}), subtotal=subtotal, product=product, cart=cart)
        
        session.add(order)
        session.commit()
        session.refresh(order)
        
        return order
        
    
    
    @staticmethod
    def remove_order(id: int, session: Session):
        order = session.get(Order, id)
        
        if order is None:
            return OrderDeleteOut(message="cart not found for given id")
        
        cart = session.get(Cart, order.cart_id)
        if cart is None:
            return OrderDeleteOut(message="No such Cart exists", data=None)
        cart.total_amount -= order.subtotal

        session.delete(order)
        session.commit()
        
        return OrderDeleteOut(message="successfully deleted cart item with given id", data=order)
        