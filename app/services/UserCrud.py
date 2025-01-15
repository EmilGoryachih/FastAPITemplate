from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.UserRepository import UserRepository
from app.models.dbModels.User.UserEntity import UserEntity as User
from uuid import uuid4

from app.services.authorization import AuthService


async def add_user(username: str, email: str, password: str, session: AsyncSession) -> User:
    user_repo = UserRepository(session)
    user = await user_repo.find_by_email(email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given email already exist",
        )
    auth = AuthService()
    hashed_password = auth.get_password_hash(password)
    new_user = User(
        id=uuid4(),
        username=username,
        email=email,
        hashed_password=hashed_password,
    )

    await user_repo.add_user(new_user)
    return new_user
