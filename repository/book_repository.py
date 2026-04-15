from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.book_model import Book
from datetime import datetime


class BookRepository:

    async def get_all(
            self,
            session: AsyncSession,
            cursor: str | None = None,
            limit: int = 10,
            status: str | None = None,
            author: str | None = None,
            sort_by: str | None = None
    ):
        """
        Get books with cursor-based pagination.

        Args:
            cursor: ISO format datetime string of the last book's created_at (for next page)
            limit: Number of items to return
            status: Filter by status
            author: Filter by author
            sort_by: Sort field (title or year)
        """
        stmt = select(Book)

        if status:
            stmt = stmt.where(Book.status == status)
        if author:
            stmt = stmt.where(Book.author == author)

        # Apply cursor filtering (get books created after the cursor)
        if cursor:
            cursor_datetime = datetime.fromisoformat(cursor)
            stmt = stmt.where(Book.created_at > cursor_datetime)

        # Sorting
        if sort_by == "title":
            stmt = stmt.order_by(Book.title)
        elif sort_by == "year":
            stmt = stmt.order_by(Book.year)
        else:
            stmt = stmt.order_by(Book.created_at)  # Default sort by creation time

        # Get limit + 1 to determine if there are more results
        stmt = stmt.limit(limit + 1)

        result = await session.execute(stmt)
        books = result.scalars().all()

        # Check if there are more results
        has_more = len(books) > limit
        if has_more:
            books = books[:limit]

        return books, has_more

    async def create(self, session: AsyncSession, book: Book):
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def delete(self, session: AsyncSession, book_id: str):
        await session.execute(delete(Book).where(Book.id == book_id))
        await session.commit()