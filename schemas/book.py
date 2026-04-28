from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    """Схема для створення книги"""
    title: str = Field(..., min_length=1, description="Назва книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    isbn: str = Field(..., description="ISBN код")
    pages: int = Field(..., gt=0, description="Кількість сторінок")
    year: int = Field(..., description="Рік видання")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "0132350882",
                "pages": 464,
                "year": 2008
            }
        }


class BookResponse(BaseModel):
    """Схема для відповіді про книгу"""
    id: Optional[str] = Field(alias="_id", default=None, description="ID книги в MongoDB")
    title: str = Field(..., description="Назва книги")
    author: str = Field(..., description="Автор книги")
    isbn: str = Field(..., description="ISBN код")
    pages: int = Field(..., description="Кількість сторінок")
    year: int = Field(..., description="Рік видання")

    class Config:
        populate_by_name = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "0132350882",
                "pages": 464,
                "year": 2008
            }
        }