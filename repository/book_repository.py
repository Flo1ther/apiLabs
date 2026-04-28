from db.database import Database
from models.book_model import Book
from bson import ObjectId
from typing import List, Optional


class BookRepository:

    def __init__(self):
        self.db = Database.get_db()
        self.collection = self.db.books

    def create(self, book: Book) -> str:
        """Створити нову книгу"""
        result = self.collection.insert_one(book.to_dict())
        return str(result.inserted_id)

    def get_all(self) -> List[dict]:
        """Отримати всі книги"""
        books = []
        for book in self.collection.find():
            book["_id"] = str(book["_id"])  # Конвертуємо ObjectId в строку
            books.append(book)
        return books

    def get_by_id(self, book_id: str) -> Optional[dict]:
        """Отримати книгу за ID"""
        try:
            obj_id = ObjectId(book_id)
            book = self.collection.find_one({"_id": obj_id})
            if book:
                book["_id"] = str(book["_id"])
                return book
        except Exception as e:
            print(f"Помилка при отриманні книги: {e}")
        return None

    def update(self, book_id: str, book_data: dict) -> bool:
        """Оновити книгу"""
        try:
            obj_id = ObjectId(book_id)
            result = self.collection.update_one(
                {"_id": obj_id},
                {"$set": book_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Помилка при оновленні книги: {e}")
        return False

    def delete(self, book_id: str) -> bool:
        """Видалити книгу"""
        try:
            obj_id = ObjectId(book_id)
            result = self.collection.delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Помилка при видаленні книги: {e}")
        return False