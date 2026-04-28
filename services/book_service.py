from repository.book_repository import BookRepository
from models.book_model import Book
from typing import List, Optional


class BookService:

    def __init__(self):
        self.repository = BookRepository()

    def create_book(self, title: str, author: str, isbn: str, pages: int, year: int) -> str:
        """Створити книгу"""
        book = Book(title=title, author=author, isbn=isbn, pages=pages, year=year)
        return self.repository.create(book)

    def get_all_books(self) -> List[dict]:
        """Отримати всі книги"""
        return self.repository.get_all()

    def get_book(self, book_id: str) -> Optional[dict]:
        """Отримати книгу по ID"""
        return self.repository.get_by_id(book_id)

    def update_book(self, book_id: str, title: str = None, author: str = None,
                    isbn: str = None, pages: int = None, year: int = None) -> bool:
        """Оновити книгу"""
        update_data = {}
        if title:
            update_data["title"] = title
        if author:
            update_data["author"] = author
        if isbn:
            update_data["isbn"] = isbn
        if pages:
            update_data["pages"] = pages
        if year:
            update_data["year"] = year

        return self.repository.update(book_id, update_data)

    def delete_book(self, book_id: str) -> bool:
        """Видалити книгу"""
        return self.repository.delete(book_id)