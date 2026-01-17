from sqlalchemy import (
    Column,
    Integer,
    String, 
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base

#---Enums---
class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"

class OrderStatus(enum.Enum):
    pending = "pending"
    cancelled = "cancelled"
    delivered = "delivered"
    shipped = "shipped"


#--- SQLAlchemy models--
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.customer.value
    )
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    orders = relationship("Order",back_populates="user")
    
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    inventory = relationship("Inventory", back_populates="product", uselist=False) # one-to-one 
    items = relationship("OrderItem", back_populates="product", uselist=True) # one-to-many
    
class Inventory(Base):
    __tablename__ = "inventories"
    
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, primary_key=True) 
    available_qty = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    product = relationship("Product", back_populates="inventory")
    
    
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending.value)
    total_amount = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True),default=func.now())
    
    user = relationship("User",back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10,2), nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")
    