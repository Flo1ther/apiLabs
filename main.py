from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from api.books import router as books_router
from api.auth import router as auth_router
from db.database import engine
from db.redis import redis_client
from models.book_model import Base
from services.rate_limiter import RateLimiter



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(" Database tables created")

    yield

    print(" Application shutting down")


app = FastAPI(
    title="Books API",
    description="API з JWT авторизацією та пагінацією",
    version="2.0.0",
    lifespan=lifespan
)

app.state.rate_limiter = RateLimiter(redis_client)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    try:
        await request.app.state.rate_limiter.check(request)
        response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )


app.include_router(auth_router)
app.include_router(books_router)


@app.get("/")
async def root():
    return {
        "message": "Books API v2.0",
        "docs": "/docs",
        "register": "/auth/register",
        "login": "/auth/login"
    }