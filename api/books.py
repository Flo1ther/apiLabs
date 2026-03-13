from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List, Optional

from schemas.book import Book, BookCreate
from services import book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[Book])
async def get_books(status: Optional[str] = None,
                    author: Optional[str] = None,
                    sort_by: Optional[str] = None):

    return await book_service.list_books(status, author, sort_by)


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID):

    book = await book_service.get_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):

    return await book_service.create_book(book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):

    await book_service.delete_book(book_id)

    return
