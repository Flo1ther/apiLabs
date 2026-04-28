import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongo_admin:password@localhost:27017")
    DATABASE_NAME = "books_db"
    JSON_SORT_KEYS = False
    RESTFUL_JSON = {"indent": 2}