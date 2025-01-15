from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy import MetaData

# Создаём объект metadata
metadata = MetaData()

@as_declarative(metadata=metadata)
class EntityDB:
    """
    Базовая модель для всех ORM-моделей.
    """
    metadata = None

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Автоматически задаёт имя таблицы, если не указано явно.
        """
        return cls.__name__.lower()
