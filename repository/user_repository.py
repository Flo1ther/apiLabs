from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.book_model import User
from db.auth import AuthService


class UserRepository:

    async def create(self, session: AsyncSession, username: str, email: str, password: str):
        # Перевірити, чи користувач уже існує
        existing = await session.execute(
            select(User).where((User.username == username) | (User.email == email))
        )
        if existing.scalars().first():
            raise ValueError("Користувач з цим іменем або email уже існує")

        hashed_password = AuthService.hash_password(password)
        user = User(username=username, email=email, password=hashed_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_username(self, session: AsyncSession, username: str):
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def verify_user(self, session: AsyncSession, username: str, password: str):
        user = await self.get_by_username(session, username)
        if not user:
            return None

        if not AuthService.verify_password(password, user.password):
            return None

        return user