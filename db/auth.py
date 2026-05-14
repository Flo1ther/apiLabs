import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class AuthService:
    SECRET_KEY = Config.SECRET_KEY
    ALGORITHM = "HS256"

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_token(
        cls,
        data: dict,
        expires_delta: timedelta,
        token_type: str
    ) -> str:
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta

        to_encode.update({
            "exp": expire,
            "type": token_type
        })

        return jwt.encode(
            to_encode,
            cls.SECRET_KEY,
            algorithm=cls.ALGORITHM
        )

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        return cls.create_token(
            data=data,
            expires_delta=timedelta(minutes=15),
            token_type="access"
        )

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        return cls.create_token(
            data=data,
            expires_delta=timedelta(days=7),
            token_type="refresh"
        )

    @classmethod
    def verify_token(
        cls,
        token: str,
        expected_type: str = "access"
    ) -> dict:
        try:
            payload = jwt.decode(
                token,
                cls.SECRET_KEY,
                algorithms=[cls.ALGORITHM]
            )

            if payload.get("type") != expected_type:
                raise HTTPException(
                    status_code=401,
                    detail="Невірний тип токена"
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Термін дії токена закінчився"
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Невалідний токен"
            )


async def get_current_user(credentials=Depends(security)) -> dict:
    token = credentials.credentials
    payload = AuthService.verify_token(token, expected_type="access")
    return payload