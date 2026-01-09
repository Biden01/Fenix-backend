# backend/main.py
# Полностью рабочая версия с правильным CORS

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uvicorn

# Создаем приложение
app = FastAPI(
    title="Fenix International API",
    description="REST API для MLM платформы",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==========================================
# КРИТИЧНО! CORS ДОЛЖЕН БЫТЬ ПЕРВЫМ!
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:8082",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
    expose_headers=["*"]
)


# ========== МОДЕЛИ ДАННЫХ ==========

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    sponsor_id: str
    city: str
    password: str
    password_confirmation: str
    partnership_type: str
    agree_terms: bool = True


class LoginRequest(BaseModel):
    user_id: str
    password: str
    remember_me: bool = False


# ========== КОРНЕВЫЕ РОУТЫ ==========

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Fenix International API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "categories": "/api/v1/shop/categories",
            "products": "/api/v1/shop/products"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# ========== АУТЕНТИФИКАЦИЯ ==========

@app.post("/api/v1/auth/register")
async def register(data: RegisterRequest):
    """Регистрация нового пользователя"""
    print(f"📝 Регистрация: {data.email}")

    # Проверка паролей
    if data.password != data.password_confirmation:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    # Генерируем ID
    user_id = f"ID{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "success": True,
        "token": f"token_{user_id}",
        "user": {
            "id": user_id,
            "full_name": data.full_name,
            "email": data.email,
            "phone": data.phone,
            "city": data.city,
            "partnership_type": data.partnership_type,
            "status": "active",
            "balance": 0,
            "bonus_balance": 0
        }
    }


@app.post("/api/v1/auth/login")
async def login(data: LoginRequest):
    """Авторизация пользователя"""
    print(f"🔐 Вход: {data.user_id}")

    return {
        "success": True,
        "token": f"token_{data.user_id}",
        "user": {
            "id": data.user_id,
            "full_name": "Тестовый Пользователь",
            "email": "test@example.com",
            "partnership_type": "leader",
            "status": "active",
            "balance": 50000,
            "bonus_balance": 1500
        }
    }


@app.post("/api/v1/auth/logout")
async def logout():
    """Выход"""
    return {"success": True, "message": "Выход выполнен"}


# ========== МАГАЗИН - КАТЕГОРИИ ==========

@app.get("/api/v1/shop/categories")
async def get_categories():
    """Получить список категорий"""
    print("📦 Запрос категорий")

    return {
        "success": True,
        "data": [
            {
                "id": 1,
                "name": "Косметика",
                "slug": "cosmetics",
                "image_url": "/images/categories/cosmetics.jpg",
                "product_count": 25
            },
            {
                "id": 2,
                "name": "Леденцы",
                "slug": "candies",
                "image_url": "/images/categories/candies.jpg",
                "product_count": 15
            },
            {
                "id": 3,
                "name": "Витамины",
                "slug": "vitamins",
                "image_url": "/images/categories/vitamins.jpg",
                "product_count": 30
            },
            {
                "id": 4,
                "name": "Батончики",
                "slug": "bars",
                "image_url": "/images/categories/bars.jpg",
                "product_count": 12
            }
        ]
    }


# ========== МАГАЗИН - ПРОДУКТЫ ==========

@app.get("/api/v1/shop/products")
async def get_products(
        category_id: Optional[int] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "popular",
        search: Optional[str] = None
):
    """Получить список продуктов"""
    print(f"🛍️ Запрос продуктов (категория: {category_id})")

    # Тестовые данные
    all_products = [
        {
            "id": "prod_001",
            "name": "Крем для лица антивозрастной",
            "description": "Натуральный крем для ежедневного ухода",
            "price": 8500,
            "old_price": 12000,
            "discount_percent": 30,
            "currency": "KZT",
            "category_id": 1,
            "category_name": "Косметика",
            "images": ["/images/products/cream1.jpg"],
            "in_stock": True,
            "stock_quantity": 50,
            "bonus_points": 85,
            "rating": 4.5,
            "reviews_count": 23
        },
        {
            "id": "prod_002",
            "name": "Витамины группы B",
            "description": "Комплекс витаминов для энергии",
            "price": 5500,
            "old_price": None,
            "discount_percent": 0,
            "currency": "KZT",
            "category_id": 3,
            "category_name": "Витамины",
            "images": ["/images/products/vitamins1.jpg"],
            "in_stock": True,
            "stock_quantity": 100,
            "bonus_points": 55,
            "rating": 4.8,
            "reviews_count": 45
        },
        {
            "id": "prod_003",
            "name": "Леденцы с медом",
            "description": "Натуральные леденцы для горла",
            "price": 1200,
            "old_price": 1500,
            "discount_percent": 20,
            "currency": "KZT",
            "category_id": 2,
            "category_name": "Леденцы",
            "images": ["/images/products/candy1.jpg"],
            "in_stock": True,
            "stock_quantity": 200,
            "bonus_points": 12,
            "rating": 4.3,
            "reviews_count": 67
        },
        {
            "id": "prod_004",
            "name": "Протеиновый батончик",
            "description": "Батончик с высоким содержанием белка",
            "price": 800,
            "old_price": None,
            "discount_percent": 0,
            "currency": "KZT",
            "category_id": 4,
            "category_name": "Батончики",
            "images": ["/images/products/bar1.jpg"],
            "in_stock": True,
            "stock_quantity": 150,
            "bonus_points": 8,
            "rating": 4.6,
            "reviews_count": 34
        },
        {
            "id": "prod_005",
            "name": "Сыворотка для лица",
            "description": "Увлажняющая сыворотка",
            "price": 12000,
            "old_price": 15000,
            "discount_percent": 20,
            "currency": "KZT",
            "category_id": 1,
            "category_name": "Косметика",
            "images": ["/images/products/serum1.jpg"],
            "in_stock": True,
            "stock_quantity": 30,
            "bonus_points": 120,
            "rating": 4.7,
            "reviews_count": 18
        },
        {
            "id": "prod_006",
            "name": "Витамин C",
            "description": "Для укрепления иммунитета",
            "price": 3500,
            "old_price": None,
            "discount_percent": 0,
            "currency": "KZT",
            "category_id": 3,
            "category_name": "Витамины",
            "images": ["/images/products/vitamin_c.jpg"],
            "in_stock": True,
            "stock_quantity": 120,
            "bonus_points": 35,
            "rating": 4.9,
            "reviews_count": 89
        }
    ]

    # Фильтрация по категории
    if category_id:
        products = [p for p in all_products if p["category_id"] == category_id]
    else:
        products = all_products

    return {
        "success": True,
        "data": products,
        "pagination": {
            "current_page": page,
            "total_pages": 1,
            "total_items": len(products),
            "items_per_page": limit
        }
    }


@app.get("/api/v1/shop/products/{product_id}")
async def get_product(product_id: str):
    """Получить детали продукта"""
    print(f"🔍 Запрос продукта: {product_id}")

    return {
        "success": True,
        "data": {
            "id": product_id,
            "name": "Крем для лица антивозрастной",
            "full_description": "Натуральный крем с органическими компонентами для ежедневного ухода за кожей лица. Подходит для всех типов кожи. Содержит витамины A, E и натуральные масла.",
            "price": 8500,
            "old_price": 12000,
            "discount_percent": 30,
            "currency": "KZT",
            "category": {"id": 1, "name": "Косметика"},
            "images": [
                "/images/products/cream1.jpg",
                "/images/products/cream2.jpg"
            ],
            "in_stock": True,
            "stock_quantity": 50,
            "bonus_points": 85,
            "specifications": {
                "volume": "50ml",
                "origin": "Казахстан",
                "ingredients": "Натуральные компоненты",
                "shelf_life": "24 месяца"
            },
            "reviews": [],
            "rating": 4.5,
            "reviews_count": 23
        }
    }


# ========== КОРЗИНА ==========

@app.post("/api/v1/shop/cart/add")
async def add_to_cart(item: dict):
    """Добавить в корзину"""
    product_id = item.get("product_id")
    quantity = item.get("quantity", 1)

    print(f"🛒 Добавление в корзину: {product_id} x{quantity}")

    return {
        "success": True,
        "cart": {
            "items": [
                {
                    "product_id": product_id,
                    "name": "Крем для лица",
                    "image": "/images/products/cream1.jpg",
                    "quantity": quantity,
                    "price": 8500,
                    "subtotal": 8500 * quantity
                }
            ],
            "total": 8500 * quantity,
            "bonus_points_earned": 85 * quantity,
            "min_order_amount": 10000,
            "is_valid_for_checkout": (8500 * quantity) >= 10000
        }
    }


@app.get("/api/v1/shop/cart")
async def get_cart():
    """Получить корзину"""
    return {
        "success": True,
        "cart": {
            "items": [],
            "total": 0,
            "min_order_amount": 10000,
            "is_valid_for_checkout": False
        }
    }


# ========== ЛИЧНЫЙ КАБИНЕТ ==========

@app.get("/api/v1/cabinet/dashboard")
async def get_dashboard():
    """Дашборд личного кабинета"""
    print("📊 Запрос дашборда")

    return {
        "success": True,
        "data": {
            "user": {
                "id": "TEST123",
                "full_name": "Тестовый Пользователь",
                "email": "test@example.com",
                "partnership_type": "leader",
                "status": "active"
            },
            "balances": {
                "main_balance": 50000,
                "bonus_balance": 1500,
                "frozen_balance": 5000,
                "currency": "KZT"
            },
            "statistics": {
                "total_orders": 25,
                "total_purchases": 125000,
                "total_earnings": 45000,
                "active_referrals": 12,
                "team_size": 35
            },
            "recent_activities": []
        }
    }


# ========== ЗАПУСК ==========

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )