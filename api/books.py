from flask import request, jsonify
from flask_restful import Resource, reqparse
from functools import wraps
from services.book_service import BookService
from services.auth_service import AuthService
from schemas.book import validate_book_create, validate_book_update

book_service = BookService()


def token_required(f):
    """Декоратор для перевірки access token"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Отримати token з заголовка Authorization
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return {"error": "Invalid token format"}, 401

        if not token:
            return {"error": "Token is missing"}, 401

        is_valid, user_id = AuthService.verify_token(token, token_type="access")
        if not is_valid:
            return {"error": "Invalid or expired token"}, 401

        kwargs["user_id"] = user_id
        return f(*args, **kwargs)

    return decorated


class BookList(Resource):

    def get(self, user_id=None):
        """
        Отримати всі книги
        ---
        tags:
          - Books
        security:
          - Bearer: []
        responses:
          200:
            description: Список всіх книг
          401:
            description: Unauthorized
        """
        books = book_service.get_all_books()
        return {"books": books, "count": len(books)}, 200

    @token_required
    def post(self, user_id=None):
        """
        Створити нову книгу
        ---
        tags:
          - Books
        security:
          - Bearer: []
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
        responses:
          201:
            description: Книга успішно створена
          400:
            description: Помилка валідації
          401:
            description: Unauthorized
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

    @token_required
    def get(self, book_id, user_id=None):
        """
        Отримати книгу по ID
        ---
        tags:
          - Books
        security:
          - Bearer: []
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
          401:
            description: Unauthorized
        """
        book = book_service.get_book(book_id)
        if not book:
            return {"error": "Книга не знайдена"}, 404
        return book, 200

    @token_required
    def put(self, book_id, user_id=None):
        """
        Оновити книгу
        ---
        tags:
          - Books
        security:
          - Bearer: []
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
          401:
            description: Unauthorized
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

    @token_required
    def delete(self, book_id, user_id=None):
        """
        Видалити книгу
        ---
        tags:
          - Books
        security:
          - Bearer: []
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
          401:
            description: Unauthorized
        """
        if book_service.delete_book(book_id):
            return "", 204
        return {"error": "Книга не знайдена"}, 404