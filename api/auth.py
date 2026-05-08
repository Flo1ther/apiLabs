from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.get("/test")
async def test_auth():
    return {"message": "auth router works"}


@router.post("/register")
async def register(user: UserRegister):
    return {
        "message": "Користувач успішно зареєстрований",
        "username": user.username
    }


@router.post("/login")
async def login(user: UserLogin):
    if user.username == "admin" and user.password == "admin":
        return {
            "access_token": "test_token",
            "token_type": "bearer"
        }

    raise HTTPException(
        status_code=401,
        detail="Невірний логін або пароль"
    )