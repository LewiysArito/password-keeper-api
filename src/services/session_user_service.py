from typing import Any, Optional
import redis.asyncio as redis
from src.config.redis.redis_helper import redis_helper

class UserSessionRedisService:
    """
    Данный сервис нужен для того, чтобы управлять сессиями пользователей
    """

    async def add(self, user_id: int, session_id:int) -> None:
        """
        Добавляет сессию
        """
        async with redis_helper.get_db_session() as session:
            await session.sadd(f"user:sessions:{user_id}", session_id)

    async def exists(self, user_id:int, session_id:int) -> Optional[bool]:
        """
        Проверяет сессию на существование
        """
        async with redis_helper.get_db_session() as session:
            is_member = await session.smismember(f"user:sessions:{user_id}", session_id)
            return bool(int(is_member))

    async def delete(self, user_id:int, session_id:int) -> None:
        """
        Удаляет сессию
        """
        async with redis_helper.get_db_session() as session:
            await session.srem(f"user:sessions:{user_id}", session_id)
    
    async def delete(self, user_id:int) -> None:
        """
        Удаляет сессию
        """
        async with redis_helper.get_db_session() as session:
            await session.delete(f"user:sessions:{user_id}")