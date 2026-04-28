from pymongo import MongoClient
from config import Config


class Database:
    client = None
    db = None

    @classmethod
    def connect(cls):
        """Підключитися до MongoDB"""
        try:
            cls.client = MongoClient(Config.MONGODB_URL)
            cls.db = cls.client[Config.DATABASE_NAME]
            # Перевіримо з'єднання
            cls.client.server_info()
            print("✅ Підключено до MongoDB")
        except Exception as e:
            print(f"❌ Помилка підключення до MongoDB: {e}")

    @classmethod
    def disconnect(cls):
        """Відключитися від MongoDB"""
        if cls.client:
            cls.client.close()
            print("✅ Відключено від MongoDB")

    @classmethod
    def get_db(cls):
        """Отримати об'єкт бази даних"""
        if cls.db is None:
            cls.connect()
        return cls.db