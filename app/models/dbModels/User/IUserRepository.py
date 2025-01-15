from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.models import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def find_by_username(self, username: str) -> UserEntity:
        """Найти пользователя по имени пользователя."""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[dict]:
        """Найти пользователя по email."""
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[dict]:
        """Найти пользователя по ID."""
        pass

    @abstractmethod
    async def find_all(self) -> List[dict]:
        """Получить всех пользователей."""
        pass

    @abstractmethod
    async def add_user(self, new_user: UserEntity) -> dict:
        """Добавить нового пользователя."""
        pass

    @abstractmethod
    async def get_hashed_password(self, user_name: str) -> str:
        """Получить хэшированный пароль"""
        pass