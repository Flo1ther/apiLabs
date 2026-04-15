from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from services.book_service import BookService
from schemas.book import BookCreate, PaginatedBooksResponse, BookResponse
from db.database import get_session
from typing import Optional

router = APIRouter(prefix="/books", tags=["books"])
service = BookService()

@router.post("", status_code=201, response_model=BookResponse)
async def create_book(
    data: BookCreate,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_book(session, data)

@router.get("", response_model=PaginatedBooksResponse)
async def get_books(
    cursor: Optional[str] = Query(None, description="Cursor for pagination (ISO format datetime)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    author: Optional[str] = Query(None, description="Filter by author"),
    sort_by: Optional[str] = Query(None, description="Sort by: title or year"),
    session: AsyncSession = Depends(get_session)
):
    result = await service.get_books(
        session=session,
        cursor=cursor,
        limit=limit,
        status=status,
        author=author,
        sort_by=sort_by
    )
    return result