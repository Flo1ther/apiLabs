from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.book_model import Book

class BookRepository:

    async def get_all(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        status: str | None,
        author: str | None,
        sort_by: str | None
    ):
        stmt = select(Book)

        if status:
            stmt = stmt.where(Book.status == status)
        if author:
            stmt = stmt.where(Book.author == author)

        if sort_by == "title":
            stmt = stmt.order_by(Book.title)
        elif sort_by == "year":
            stmt = stmt.order_by(Book.year)

        stmt = stmt.limit(limit).offset(offset)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def create(self, session: AsyncSession, book: Book):
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def delete(self, session: AsyncSession, book_id: str):
        await session.execute(delete(Book).where(Book.id == book_id))
        await session.commit()