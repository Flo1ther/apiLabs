from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from contextlib import asynccontextmanager
from api.books import router as books_router
import os

# Використовуємо MongoDB Atlas замість локального
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://mira_db:<db_password>@cluster0.atifi0s.mongodb.net/?appName=Cluster0"
)
DATABASE_NAME = "books_db"

client: AsyncIOMotorClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global client
    try:
        client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        await client.server_info()
        print("✅ Підключено до MongoDB Atlas")
    except Exception as e:
        print(f"⚠️ Помилка підключення до MongoDB: {e}")

    yield

    # Shutdown
    if client:
        client.close()
        print("✅ MongoDB з'єднання закрито")


app = FastAPI(
    title="Books API",
    description="CRUD API для управління книгами на MongoDB",
    version="1.0.0",
    lifespan=lifespan
)


def get_database() -> AsyncIOMotorDatabase:
    """Отримати базу даних"""
    if client is None:
        raise Exception("MongoDB недоступна")
    return client[DATABASE_NAME]


app.dependency_overrides[AsyncIOMotorDatabase] = get_database
app.include_router(books_router)


@app.get("/")
async def root():
    """Корневий ендпоінт"""
    return {
        "message": "Ласкаво просимо до Books API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Перевірка здоров'я API"""
    try:
        if client:
            await client.server_info()
            return {"status": "ok", "database": "connected"}
    except:
        pass
    return {"status": "ok", "database": "disconnected"}