from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    language_code = Column(String(10), default="ru")
    referral_code = Column(String(32), unique=True)
    referred_by = Column(Integer)
    balance = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, index=True)
    product_type = Column(String(50), nullable=False)  # premium, stars, nft
    product_id = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(50), default="pending")  # pending, paid, delivered, cancelled
    invoice_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), index=True)  # premium, stars, nft
    product_id = Column(String(100), unique=True)
    name = Column(String(255))
    price = Column(Float)
    description = Column(Text)
    is_active = Column(Boolean, default=True)