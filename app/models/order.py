from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.sql import func
from app.database import Base
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum.Enum):
    CARD = "card"
    CASH = "cash"
    BALANCE = "balance"
    BONUS = "bonus"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    order_number = Column(String(50), unique=True)
    user_id = Column(String, ForeignKey("users.id"))

    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(Enum(PaymentMethod))
    payment_status = Column(String(50), default="pending")

    items = Column(JSON)  # Список товаров
    customer_info = Column(JSON)
    delivery_address = Column(JSON)

    subtotal = Column(Float, default=0.0)
    delivery_cost = Column(Float, default=0.0)
    bonus_used = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    bonus_earned = Column(Integer, default=0)

    tracking_number = Column(String(100), nullable=True)
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)