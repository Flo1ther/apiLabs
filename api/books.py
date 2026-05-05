from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from services.book_service import BookService
from repository.book_repository import BookRepository
from schemas.book import BookCreate, BookResponse
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=List[BookResponse])
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = None,
    author: str | None = None,
    sort_by: str | None = Query(None, pattern="^(title|year)$"),
    session: AsyncSession = Depends(get_session),
):
    repo = BookRepository()
    return await repo.get_all(session, limit, offset, status, author, sort_by)


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    data: BookCreate,
    session: AsyncSession = Depends(get_session),
):
    service = BookService()
    return await service.create_book(session, data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
):
    repo = BookRepository()
    deleted_count = await repo.delete(session, book_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )