from models.book_model import Book
from repository.book_repository import BookRepository
from schemas.book import BookCreate


class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def create_book(self, session, data: BookCreate):
        book = Book(**data.model_dump())
        return await self.repo.create(session, book)

    async def get_books(
            self,
            session,
            cursor: str | None = None,
            limit: int = 10,
            status: str | None = None,
            author: str | None = None,
            sort_by: str | None = None
    ):
        books, has_more = await self.repo.get_all(
            session=session,
            cursor=cursor,
            limit=limit,
            status=status,
            author=author,
            sort_by=sort_by
        )

        # Get the next cursor from the last book
        next_cursor = None
        if books and has_more:
            next_cursor = books[-1].created_at.isoformat()

        return {
            "data": books,
            "cursor": next_cursor,
            "has_more": has_more
        }