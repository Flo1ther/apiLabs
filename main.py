from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flasgger import Flasgger
from db.database import Database
from api.books import BookList, BookDetail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

swagger = Flasgger(app)

api = Api(app)

api.add_resource(BookList, "/api/books", endpoint="books")
api.add_resource(BookDetail, "/api/books/<string:book_id>", endpoint="book")

@app.route("/")
def index():
    return jsonify({
        "message": "Ласкаво просимо до Books API",
        "docs": "/apidocs",
        "health": "/health"
    })

@app.route("/health")
def health():
    try:
        Database.get_db()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except:
        return jsonify({"status": "ok", "database": "disconnected"}), 200

@app.before_request
def before_request():
    Database.connect()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)