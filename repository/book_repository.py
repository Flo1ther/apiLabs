from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.book import BookCreate, BookResponse
from typing import List, Optional
from bson import ObjectId


class BookRepository:
    """Репозиторій для роботи з книгами в MongoDB"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.books

    async def create(self, book: BookCreate) -> BookResponse:
        """Створити нову книгу"""
        book_dict = book.dict()
        result = await self.collection.insert_one(book_dict)
        book_dict["_id"] = str(result.inserted_id)
        return BookResponse(**book_dict)

    async def get_all(self) -> List[BookResponse]:
        """Отримати всі книги"""
        books = await self.collection.find({}).to_list(None)
        return [BookResponse(_id=str(book["_id"]), **{k: v for k, v in book.items() if k != "_id"})
                for book in books]

    async def get_by_id(self, book_id: str) -> Optional[BookResponse]:
        """Отримати книгу за ID"""
        try:
            obj_id = ObjectId(book_id)
            book = await self.collection.find_one({"_id": obj_id})
            if book:
                return BookResponse(_id=str(book["_id"]), **{k: v for k, v in book.items() if k != "_id"})
        except Exception as e:
            print(f"Помилка при отриманні книги: {e}")
        return None

    async def update(self, book_id: str, book: BookCreate) -> Optional[BookResponse]:
        """Оновити книгу"""
        try:
            obj_id = ObjectId(book_id)
            result = await self.collection.find_one_and_update(
                {"_id": obj_id},
                {"$set": book.dict()},
                return_document=True
            )
            if result:
                return BookResponse(_id=str(result["_id"]), **{k: v for k, v in result.items() if k != "_id"})
        except Exception as e:
            print(f"Помилка при оновленні книги: {e}")
        return None

    async def delete(self, book_id: str) -> bool:
        """Видалити книгу"""
        try:
            obj_id = ObjectId(book_id)
            response = await self.collection.delete_one({"_id": obj_id})
            return response.deleted_count > 0
        except Exception as e:
            print(f"Помилка при видаленні книги: {e}")
        return False