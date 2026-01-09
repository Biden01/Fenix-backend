from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services.auth import AuthService
from app.models.user import User
from sqlalchemy import select
import secrets

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существующего email
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Проверка спонсора
    if user_data.sponsor_id:
        sponsor = await db.execute(select(User).where(User.id == user_data.sponsor_id))
        if not sponsor.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Invalid sponsor ID")

    # Создание пользователя
    user_id = f"ID{datetime.now().strftime('%Y%m%d%H%M%S')}"
    referral_code = secrets.token_urlsafe(8).upper()

    new_user = User(
        id=user_id,
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        city=user_data.city,
        hashed_password=AuthService.get_password_hash(user_data.password),
        partnership_type=user_data.partnership_type,
        sponsor_id=user_data.sponsor_id,
        referral_code=referral_code
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Создание токена
    access_token = AuthService.create_access_token(data={"sub": user_id})

    return TokenResponse(
        token=access_token,
        user=new_user
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == credentials.user_id))
    user = result.scalar_one_or_none()

    if not user or not AuthService.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expires_delta = timedelta(days=30) if credentials.remember_me else None
    access_token = AuthService.create_access_token(
        data={"sub": user.id},
        expires_delta=expires_delta
    )

    return TokenResponse(
        token=access_token,
        user=user
    )