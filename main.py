from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from flasgger import Flasgger
from db.database import Database
from api.books import BookList, BookDetail
from services.auth_service import AuthService
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

swagger = Flasgger(app)

api = Api(app)

api.add_resource(BookList, "/api/books", endpoint="books")
api.add_resource(BookDetail, "/api/books/<string:book_id>", endpoint="book")


@app.route("/auth/login", methods=["POST"])
def login():
    """
    Вхід та отримання токенів
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: string
              example: "user123"
          required:
            - user_id
    responses:
      200:
        description: Токени успішно створені
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            token_type:
              type: string
      400:
        description: Помилка валідації
    """
    data = request.get_json()

    if not data or "user_id" not in data:
        return {"error": "user_id is required"}, 400

    user_id = data.get("user_id")

    access_token = AuthService.create_access_token(user_id)
    refresh_token = AuthService.create_refresh_token(user_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }, 200


@app.route("/auth/refresh", methods=["POST"])
def refresh():
    """
    Оновити access token
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            refresh_token:
              type: string
          required:
            - refresh_token
    responses:
      200:
        description: Новий access token
        schema:
          type: object
          properties:
            access_token:
              type: string
            token_type:
              type: string
      401:
        description: Invalid или expired refresh token
    """
    data = request.get_json()

    if not data or "refresh_token" not in data:
        return {"error": "refresh_token is required"}, 400

    refresh_token = data.get("refresh_token")

    is_valid, access_token = AuthService.refresh_access_token(refresh_token)

    if not is_valid:
        return {"error": "Invalid or expired refresh token"}, 401

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }, 200


@app.route("/")
def index():
    """Корневий ендпоінт"""
    return jsonify({
        "message": "Ласкаво просимо до Books API",
        "docs": "/apidocs",
        "health": "/health",
        "auth": {
            "login": "/auth/login",
            "refresh": "/auth/refresh"
        }
    })


@app.route("/health")
def health():
    """
    Перевірка здоров'я API
    ---
    tags:
      - Health
    responses:
      200:
        description: API здоровий
    """
    try:
        Database.get_db()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except:
        return jsonify({"status": "ok", "database": "disconnected"}), 200


@app.before_request
def before_request():
    """Виконати перед запитом"""
    Database.connect()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)