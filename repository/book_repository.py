from models.book_model import books_storage
from uuid import UUID


async def get_all_books():
    return books_storage


async def get_book_by_id(book_id: UUID):
    for book in books_storage:
        if book["id"] == book_id:
            return book
    return None


async def add_book(book: dict):
    books_storage.append(book)
    return book


async def delete_book(book_id: UUID):
    for book in books_storage:
        if book["id"] == book_id:
            books_storage.remove(book)
            return True
    return False
