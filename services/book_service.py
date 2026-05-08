from repository.book_repository import BookRepository
from schemas.book import BookCreate, BookResponse


class BookService:
    """Сервіс для управління книгами"""

    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def create_book(self, book: BookCreate) -> BookResponse:
        """Створити нову книгу"""
        return await self.repository.create(book)

    async def get_all_books(self) -> list[BookResponse]:
        """Отримати всі книги"""
        return await self.repository.get_all()

    async def get_book(self, book_id: str) -> BookResponse:
        """Отримати книгу по ID"""
        return await self.repository.get_by_id(book_id)

    async def update_book(self, book_id: str, book: BookCreate) -> BookResponse:
        """Оновити книгу"""
        return await self.repository.update(book_id, book)

    async def delete_book(self, book_id: str) -> bool:
        """Видалити книгу"""
        return await self.repository.delete(book_id)