from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: str
    year: int

class BookResponse(BookCreate):
    id: str