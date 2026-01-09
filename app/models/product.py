from sqlalchemy import Column, String, Float, Integer, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True)
    image_url = Column(String(255))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)
    description = Column(Text)
    full_description = Column(Text)

    category_id = Column(Integer, ForeignKey("categories.id"))

    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)
    partner_price = Column(Float, nullable=True)

    stock_quantity = Column(Integer, default=0)
    in_stock = Column(Boolean, default=True)

    bonus_points = Column(Integer, default=0)
    commission_percent = Column(Float, default=10.0)

    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    views_count = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())