from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from api.books import router
from db.database import DATABASE_URL, engine
from models.book_model import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    yield

    # Shutdown code
    print("Application shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(router)