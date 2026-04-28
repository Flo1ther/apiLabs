from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService
from repository.book_repository import BookRepository
from typing import List

router = APIRouter(prefix="/books", tags=["books"])

async def get_book_service(db: AsyncIOMotorDatabase = Depends(lambda: __import__('main').db)) -> BookService:
    repository = BookRepository(db)
    return BookService(repository)

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    return await service.create_book(book)

@router.get("/", response_model=List[BookResponse])
async def get_books(service: BookService = Depends(get_book_service)):
    return await service.get_all_books()

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, service: BookService = Depends(get_book_service)):
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: str, book: BookCreate, service: BookService = Depends(get_book_service)):
    updated = await service.update_book(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: str, service: BookService = Depends(get_book_service)):
    if not await service.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")