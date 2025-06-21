from contextlib import asynccontextmanager
from typing import Optional
from src.config.redis.redis_config import settings_redis
import redis.asyncio as redis

class RedisHelper:
    """
    Класс хелпер для вспомогательных функций с Redis
    """
    
    def __init__(self, url: str):
        """
        Инициализация RedisHelper.

        :param url:  URL подключения к Redis.
        """
        self.url_connection = redis.from_url(url)
        self._client = None

    async def connect(self):
        """
        Осуществляет подключение к редису
        """
        if self._client is None:
            self._client = await redis.from_url(self.url, decode_responses=True)

    @asynccontextmanager
    async def get_db_session(self):
        """
        Асинхронный контекстный менеджер для работы с сессией Redis.
        Создает новую сессию для работы с Redis
        
        :yield: redis.Redis: Асинхронная клиент Redis
        """
        await self.connect()
        try:
            yield self._client
        finally:
            pass    

redis_helper = RedisHelper(
    settings_redis.url
)