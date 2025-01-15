from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.dbModels.User.UserEntity import UserEntity as User
from app.models.dbModels.User.IUserRepository import IUserRepository
from typing import List, Optional
from uuid import UUID



class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_username(self, username: str) -> User:
        query = select(User).where(User.name == username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def find_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def find_by_id(self, id: UUID) -> Optional[dict]:
        query = select(User).where(User.id == id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user.to_dict() if user else None

    async def find_all(self) -> List[dict]:
        query = select(User)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [user.to_dict() for user in users]

    async def add_user(self, new_user: User) -> dict:
        self.session.add(new_user)
        await self.session.commit()
        return new_user.to_dict()

    async def get_hashed_password(self, username: str) -> str:
        query = select(User).where(User.name == username)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user.hashed_password

