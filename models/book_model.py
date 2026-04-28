from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class Book(BaseModel):
    """MongoDB модель для книги"""
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    title: str
    author: str
    isbn: str
    pages: int
    year: int

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True