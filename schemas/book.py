from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: str
    year: int


class BookResponse(BookCreate):
    id: str


class PaginatedBookResponse(BaseModel):
    items: list[BookResponse]
    total: int
    limit: int
    offset: int


# User schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict