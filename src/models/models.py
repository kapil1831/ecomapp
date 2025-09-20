from sqlalchemy.orm import mapped_column, Mapped, relationship, column_property
from sqlalchemy import Integer, String, ForeignKey, Table, Column, select, JSON, Enum
from typing import Optional, List, Any
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import func
from enum import Enum as PyEnum


from .base import Base
from .users import User

product_category_association = Table(
    "products_categories", Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

class Product(Base):
    __tablename__ = 'products'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(255), default="no description")
    price: Mapped[int] 
    discount_percentage: Mapped[float] = mapped_column(default=0.0)
    rating: Mapped[float] = mapped_column(default=0.0)
    stock: Mapped[int]
    brand: Mapped[str]
    thumbnail: Mapped[Optional[str]]
    images: Mapped[str]
    is_published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    categories: Mapped[List["Category"]] = relationship(secondary=product_category_association, back_populates="products") #many to many relationship
    
    def __repr__(self):
        return f"Product(id={self.id}, title='{self.title}', price={self.price}, stock={self.stock}, categories={self.categories})"
    
class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    products: Mapped[List["Product"]] = relationship(secondary=product_category_association, back_populates="categories")  # many to many relationship
    
    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    subtotal: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
   
    
    product: Mapped[Product] = relationship()  #one to many relationship
    cart: Mapped["Cart"]  = relationship(back_populates="cart_items") # one to many relationship
    
    def __repr__(self):
        return (f"CartItem(id={self.id}, product_id={self.product_id}, "
                f"cart_id={self.cart_id}, quantity={self.quantity}, "
                f"subtotal={self.subtotal})")
    @property
    def product_price(self):
        return self.product.price

class Cart(Base):
    __tablename__ = 'carts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)     # cart should be associated to only a single user always
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    total_amount: Mapped[float] = mapped_column(default=0.0)

    user: Mapped["User"] = relationship(uselist=False) #one to one relationship
    cart_items: Mapped[List["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")  # one to many relationship
    
    def __repr__(self):
        return f"cart(id={self.id}), user_id={self.user_id}, total_amount={self.total_amount})"
    
    total_discount = column_property(
         select(
            func.coalesce(
                func.sum((Product.price * CartItem.quantity) - CartItem.subtotal),
                0.0
            )
        )
        .select_from(CartItem)
        .join(Product, Product.id == CartItem.product_id)
        .where(CartItem.cart_id == id)
        .correlate_except(CartItem)
        .scalar_subquery()
    )
    
    @property
    def item_count(self) -> int:
        return len(self.cart_items)
    
    @property
    def grand_total(self):
        return sum(cart_item.subtotal for cart_item in self.cart_items)
    
class OrderStatus(PyEnum):
    PLACED = "placed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
class PaymentStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"
    
class PaymentType(PyEnum):
    COD = "cash on delivery"
    CARD = "debit/credit cart"
    INTERNET_BANKING = "internet banking"
    UPI = "upi"
    
class Order(Base):
    __tablename__ = 'orders'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status", native_enum=False), default=OrderStatus.PLACED)
    address: Mapped[str] = mapped_column(String(200))  # can be a saperate table
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_type: Mapped[PaymentType] = mapped_column(Enum(PaymentType), default=PaymentType.COD)
    payment_details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict) # can be a saperate table
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    order_items: Mapped[list[dict]] = mapped_column(JSON, default=list) 
    order_details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user: Mapped["User"] = relationship()
    cart: Mapped["Cart"] = relationship()

    @property
    def total_order_amount(self):
        total_amount = self.order_details.get("total_amount", 0) if self.order_details is not None else 0
        return total_amount
    
    @property
    def item_count(self):
        item_count = self.order_details.get("item_count", 0) if self.order_details is not None else 0
        return item_count
    
    @property
    def subtotal(self):
        return self.order_details.get("grand_total", 0) if self.order_details is not None else 0
        
    def __repr__(self):
        return f"order(id = {self.id}, user_id)"