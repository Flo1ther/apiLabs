from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book import BookCreate, BookResponse, PaginatedBookResponse
from services.book_service import BookService
from db.database import get_session
from db.auth import get_current_user

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book: BookCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    service = BookService(session)
    return await service.create(book)


@router.get("/", response_model=PaginatedBookResponse)
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = None,
    author: str | None = None,
    sort_by: str | None = None,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    service = BookService(session)
    books = await service.get_all(limit, offset, status, author, sort_by)
    total = len(books)
    return {
        "items": books,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    service = BookService(session)
    return await service.get_by_id(book_id)


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    service = BookService(session)
    await service.delete(book_id)