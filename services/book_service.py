from datetime import datetime, UTC

from models.book_model import Book
from repository.book_repository import BookRepository
from schemas.book import BookCreate


class BookService:

    def __init__(self):
        self.repo = BookRepository()

    async def create_book(self, session, data: BookCreate):
        book = Book(
            **data.model_dump(),
            created_at=datetime.now(UTC)
        )

        return await self.repo.create(session, book)

    async def get_books(
        self,
        session,
        limit: int,
        offset: int,
        status: str | None = None,
        author: str | None = None,
        sort_by: str | None = None
    ):
        return await self.repo.get_all(
            session=session,
            limit=limit,
            offset=offset,
            status=status,
            author=author,
            sort_by=sort_by
        )

    async def get_book_by_id(self, session, book_id: str):
        return await self.repo.get_by_id(session, book_id)

    async def delete_book(self, session, book_id: str):
        return await self.repo.delete(session, book_id)