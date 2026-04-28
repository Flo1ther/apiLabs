from flask_restful import Resource, reqparse
from services.book_service import BookService
from schemas.book import validate_book_create, validate_book_update

book_service = BookService()


class BookList(Resource):

    def get(self):
        """
        Отримати всі книги
        ---
        tags:
          - Books
        responses:
          200:
            description: Список всіх книг
            schema:
              type: object
              properties:
                books:
                  type: array
                  items:
                    type: object
                count:
                  type: integer
        """
        books = book_service.get_all_books()
        return {"books": books, "count": len(books)}, 200

    def post(self):
        """
        Створити нову книгу
        ---
        tags:
          - Books
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                title:
                  type: string
                author:
                  type: string
                isbn:
                  type: string
                pages:
                  type: integer
                year:
                  type: integer
              required:
                - title
                - author
                - isbn
                - pages
                - year
        responses:
          201:
            description: Книга успішно створена
          400:
            description: Помилка валідації
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("author", type=str, required=True)
        parser.add_argument("isbn", type=str, required=True)
        parser.add_argument("pages", type=int, required=True)
        parser.add_argument("year", type=int, required=True)
        args = parser.parse_args()

        is_valid, error = validate_book_create(args)
        if not is_valid:
            return {"error": error}, 400

        book_id = book_service.create_book(**args)
        return {
            "id": book_id,
            "message": "Книга успішно створена"
        }, 201


class BookDetail(Resource):

    def get(self, book_id):
        """
        Отримати книгу по ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Дані книги
          404:
            description: Книга не знайдена
        """
        book = book_service.get_book(book_id)
        if not book:
            return {"error": "Книга не знайдена"}, 404
        return book, 200

    def put(self, book_id):
        """
        Оновити книгу
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
          - name: body
            in: body
            schema:
              type: object
              properties:
                title:
                  type: string
                author:
                  type: string
                isbn:
                  type: string
                pages:
                  type: integer
                year:
                  type: integer
        responses:
          200:
            description: Книга успішно оновлена
          404:
            description: Книга не знайдена
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("author", type=str)
        parser.add_argument("isbn", type=str)
        parser.add_argument("pages", type=int)
        parser.add_argument("year", type=int)
        args = parser.parse_args()

        update_data = {k: v for k, v in args.items() if v is not None}

        is_valid, error = validate_book_update(update_data)
        if not is_valid:
            return {"error": error}, 400

        if book_service.update_book(book_id, **update_data):
            return {"message": "Книга успішно оновлена"}, 200
        return {"error": "Книга не знайдена"}, 404

    def delete(self, book_id):
        """
        Видалити книгу
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Книга успішно видалена
          404:
            description: Книга не знайдена
        """
        if book_service.delete_book(book_id):
            return "", 204
        return {"error": "Книга не знайдена"}, 404