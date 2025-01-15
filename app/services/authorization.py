from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import fastapi_get_db
from app.models.dbModels.User.UserEntity import UserEntity
from app.models.dtoModels.TockenDTO import TokenDTO
from app.models.dtoModels.UserDTO import UserDTO
from app.infrastructure.repositories.UserRepository import UserRepository

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "7cf4d82b6f1cb0f455501cb48d22a091c3834b6d31aefd2cd7643b99ac725fb9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Настройка
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token/get-token")


class AuthService:
    """
    Сервис для обработки аутентификации и токенов.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(self, email: str, password: str, session: AsyncSession) -> UserEntity | None:
        """
        Аутентификация пользователя по email.
        """
        user_repo = UserRepository(session)
        user = await user_repo.find_by_email(email)
        if user and self.verify_password(password, user.hashed_password):
            return user
        return None

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Создание токена с email в качестве идентификатора.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def login_for_access_token(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession
    ) -> TokenDTO:
        """
        Авторизация пользователя и выдача токена.
        """
        user = await self.authenticate_user(form_data.username, form_data.password, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return TokenDTO(access_token=access_token, token_type="bearer")


async def get_current_user_service(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(fastapi_get_db),
) -> UserDTO:
    """
    Получение текущего пользователя по токену (по email).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Получение email из токена
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user_repo = UserRepository(session)
    user = await user_repo.find_by_email(email)
    if not user:
        raise credentials_exception

    return UserDTO(id=user.id, name=user.name, email=user.email)
