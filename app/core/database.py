"""
Модуль для настройки базы данных и создания сессий.
"""

from sqlalchemy import NullPool
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.config import settings

if settings.MODE == "TEST":
    DB_URL = settings.TEST_DB_URL
    DB_PARAMS = {"poolclass": NullPool}
else:
    DB_URL = settings.DB_URL
    DB_PARAMS = {}

engine = create_async_engine(DB_URL, **DB_PARAMS)

async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


class Base(DeclarativeBase):
    """
    Базовый класс для декларативного определения моделей.
    """
    pass


async def get_db():
    """
    Получение асинхронной сессии базы данных.

    - Возвращает:
        Асинхронную сессию для работы с базой данных.
    """
    async with async_session_maker() as session:
        yield session
