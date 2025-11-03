from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_type = Column(String)  # "followers" or "likes"
    quantity = Column(Integer)
    amount_usd = Column(String)  # e.g., "0.20"
    status = Column(String, default="pending")  # pending, completed, cancelled
    instagram_target = Column(String)  # username or post URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)  # 1 to 5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)  # e.g., "hero_title_ar"
    value = Column(Text)

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)
