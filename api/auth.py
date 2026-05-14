from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.auth import AuthService

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


class RefreshRequest(BaseModel):
    refresh_token: str


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

    if user.username != "admin" or user.password != "admin":
        raise HTTPException(
            status_code=401,
            detail="Невірний логін або пароль"
        )

    payload = {
        "sub": user.username
    }

    access_token = AuthService.create_access_token(payload)

    refresh_token = AuthService.create_refresh_token(payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(data: RefreshRequest):

    payload = AuthService.verify_token(
        token=data.refresh_token,
        expected_type="refresh"
    )

    username = payload.get("sub")

    new_access_token = AuthService.create_access_token({
        "sub": username
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }