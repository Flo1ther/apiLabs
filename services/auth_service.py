from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from db.auth import AuthService
from typing import Optional


class AuthenticationService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository()

    async def register(self, username: str, email: str, password: str) -> dict:
        user = await self.user_repo.create(self.session, username, email, password)
        return {"id": user.id, "message": "Користувач успішно зареєстрований"}

    async def login(self, username: str, password: str) -> Optional[dict]:
        user = await self.user_repo.verify_user(self.session, username, password)
        if not user:
            return None

        token_data = {"sub": user.id, "username": user.username}
        access_token = AuthService.create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }