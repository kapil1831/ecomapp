
import typing
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
        return OrdersOut(message="all existing orders", count = len(orders), data=orders)
    
    
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
            return OrderUpdateOut(message="No such Order exist in your order", data=None)
        
        update_data = order_payload.model_dump()
        
        for key, value in update_data.items():
            if key and value is not None:
                setattr(order, key, value)
            
        session.commit()
        session.refresh(order)
        return OrderUpdateOut(message="successfully updated the order", data=order)
            
        
    
    
    @staticmethod
    def create_order(order_payload: OrderCreate, session: Session):
        print(order_payload)
        
        cart_id = order_payload.cart_id
        user_id = order_payload.user_id
        
        cart = session.get(Cart, cart_id)
        print(cart)
        
        if cart is None:
            raise HTTPException(status_code=404, detail="cart not found for given id")
        
        user = session.get(User, user_id)        
        if user is None:
             raise HTTPException(status_code=404, detail="user not found for given id")
        
        # we assume such order does not exists and we create a new order everytime
        item_rows = []
        for ci in cart.cart_items:
            unit_price = float(ci.product.price)
            discount_pct = float(getattr(ci.product, "discount_percentage", 0.0) or 0.0)
            effective_price = unit_price * (1 - discount_pct / 100)
            item_rows.append({
                "cart_item_id": ci.id,
                "product_id": ci.product_id,
                "product_title": ci.product.title,
                "quantity": ci.quantity,
                "unit_price": unit_price,
                "discount_percentage": discount_pct,
                "price_after_discount": round(effective_price, 2),
                "line_subtotal": float(ci.subtotal),
            })

        order_details = {
            "item_count": len(item_rows),
            "total_amount": float(cart.total_amount),
            "total_discount": float(cart.total_discount),
            "grand_total": float(cart.grand_total) if hasattr(cart, "grand_total") else float(cart.total_amount - cart.total_discount),
        }
        order = Order(
            **order_payload.model_dump(exclude={"order_details", "order_items"}), 
            order_items=item_rows,
            order_details=order_details, 
        )
        
        session.add(order)
        session.commit()
        session.refresh(order)
        #[TODO] empty the cart after order is created
        
        return order
        
    
    
    @staticmethod
    def remove_order(id: int, session: Session):
        order = session.get(Order, id)
        
        if order is None:
            return OrderDeleteOut(message="order not found for given id")
        
        session.delete(order)
        session.commit()
        
        return OrderDeleteOut(message="successfully deleted order with given id", data=order)
        