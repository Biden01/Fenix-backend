from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class PartnershipType(str, enum.Enum):
    LEADER = "leader"
    CLIENT = "client"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    city = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)

    partnership_type = Column(Enum(PartnershipType), default=PartnershipType.CLIENT)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)

    sponsor_id = Column(String, nullable=True)
    referral_code = Column(String(50), unique=True)

    main_balance = Column(Float, default=0.0)
    bonus_balance = Column(Float, default=0.0)
    frozen_balance = Column(Float, default=0.0)

    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())