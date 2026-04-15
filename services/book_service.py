from models.book_model import Book
from repository.book_repository import BookRepository
from schemas.book import BookCreate

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def create_book(self, session, data: BookCreate):
        book = Book(**data.model_dump())
        return await self.repo.create(session, book)