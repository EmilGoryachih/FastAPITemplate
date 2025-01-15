from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infrastructure.core import settings
from app.models.dbModels.EntityDB import EntityDB, metadata

# Создание асинхронного двигателя
async_engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URI),
    echo=True,  # Можно оставить True для отладки
    future=True,
)

# Создание асинхронного sessionmaker
async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
)

# Создание таблиц
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

# Dependency для FastAPI
async def fastapi_get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()
