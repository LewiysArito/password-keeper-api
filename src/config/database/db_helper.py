from asyncio import current_task
from contextlib import asynccontextmanager
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)

from src.config.database.db_config import settings_db

class DatabaseHelper:
    """
    Вспомогательный класс для работы с асинхронной базой данных с использованием SQLAlchemy.

    Этот класс предоставляет методы для создания асинхронного движка базы данных, фабрики сессий
    и управления сессиями через контекстные менеджеры.

    Атрибуты:
        engine : Асинхронный движок базы данных, созданный с помощью SQLAlchemy.
        session_factory : Фабрика для создания асинхронных сессий.

    Методы:
        get_scope_session(): Возвращает сессию, привязанную к текущей задаче asyncio.
        get_db_session(): Асинхронный контекстный менеджер для работы с сессией базы данных.
    """
    
    def __init__(self, url: str, echo: bool = False):
        """
        Инициализация DatabaseHelper.

        :param url:  URL подключения к базе данных.
        :param echo: Флаг для включения логирования SQL-запросов. По умолчанию False.
        """
        self.engine = create_async_engine(url=url, echo=echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scope_session(self):
        """
        Создаёт сессию, привязанную к текущей задаче
        
        Используется для управления сессиями в рамках одной задачи. Это полезно, если
        вы хотите использовать одну и ту же сессию в разных частях кода в пределах одной задачи.

        :return: async_scoped_session: Сессия, привязанная к текущей задаче.
        """
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )

    @asynccontextmanager
    async def get_db_session(self):
        """
        Асинхронный контекстный менеджер для работы с сессией базы данных.
        Создает новую сессию для работы с базой данных.
        
        :yield: AsyncSession: Асинхронная сессия для работы с базой данных.
        """
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.close()

db_helper = DatabaseHelper(
    settings_db.database_url, 
    settings_db.DB_ECHO_LOG
)
