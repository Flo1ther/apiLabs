import jwt
from datetime import datetime, timedelta
from typing import Tuple, Optional
import os


class AuthService:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def create_access_token(cls, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm="HS256")

    @classmethod
    def create_refresh_token(cls, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm="HS256")

    @classmethod
    def verify_token(cls, token: str, token_type: str = "access") -> Tuple[bool, Optional[str]]:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"])

            if payload.get("type") != token_type:
                return False, None

            user_id = payload.get("sub")
            return True, user_id
        except jwt.ExpiredSignatureError:
            return False, None
        except jwt.InvalidTokenError:
            return False, None

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> Tuple[bool, Optional[str]]:
        is_valid, user_id = cls.verify_token(refresh_token, token_type="refresh")
        if not is_valid:
            return False, None

        new_access_token = cls.create_access_token(user_id)
        return True, new_access_token