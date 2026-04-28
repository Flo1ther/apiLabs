from bson import ObjectId


class Book:

    def __init__(self, title, author, isbn, pages, year, _id=None):
        self._id = _id if _id else ObjectId()
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pages = pages
        self.year = year

    def to_dict(self):
        """Конвертувати в словник для збереження в БД"""
        return {
            "_id": self._id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "pages": self.pages,
            "year": self.year
        }

    @staticmethod
    def from_dict(data):
        """Конвертувати зі словника"""
        return Book(
            title=data.get("title"),
            author=data.get("author"),
            isbn=data.get("isbn"),
            pages=data.get("pages"),
            year=data.get("year"),
            _id=data.get("_id")
        )