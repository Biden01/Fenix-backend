from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    city: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    sponsor_id: str
    partnership_type: str


class UserLogin(BaseModel):
    user_id: str
    password: str
    remember_me: bool = False


class UserResponse(UserBase):
    id: str
    partnership_type: str
    status: str
    main_balance: float
    bonus_balance: float
    referral_code: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    success: bool = True
    token: str
    user: UserResponse