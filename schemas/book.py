from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID
from typing import Optional


class BookStatus(str, Enum):
    available = "available"
    issued = "issued"


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: Optional[str] = None
    status: BookStatus
    year: int = Field(ge=0, le=2100)


class Book(BaseModel):
    id: UUID
    title: str
    author: str
    description: Optional[str]
    status: BookStatus
    year: int
