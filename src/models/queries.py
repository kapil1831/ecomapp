
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from ..models.models import CartItem, Cart, Product
from ..models.users import User



# manager class
class CartQuerySet:
    
    def get_all_carts(cls, session: Session):
        return session.query(CartItem).all()
    
    
if __name__ == "__main__":
    # Example usage
    with Session() as session:
        queryset = CartQuerySet()
        carts = queryset.get_all_carts(session)
        for cart in carts:
            print(cart)