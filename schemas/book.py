from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: str
    year: int


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    author: str
    description: Optional[str]
    status: str
    year: int
    created_at: datetime


class PaginatedBooksResponse(BaseModel):
    data: list[BookResponse]
    cursor: Optional[str] = None  # Next cursor for pagination
    has_more: bool