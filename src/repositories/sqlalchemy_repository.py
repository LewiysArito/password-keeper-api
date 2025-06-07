from typing import List, Type, Optional, Generic
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.base_model import ModelType
from src.repositories.base_repository import AbstractRepository
from src.schemas.base_schema import CreateSchemaType, UpdateSchemaType

class SqlAlchemyRepository(AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self._session_factory = db_session
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self._session_factory() as session:
            session: AsyncSession
            instance = self.model(**data.model_dump())
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        async with self._session_factory() as session:
            session: AsyncSession
            stmt = (
                update(self.model).
                values(**data.model_dump()).
                filter_by(**filters).
                returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> int:
        async with self._session_factory() as session:
            session: AsyncSession
            stmt = (
                delete(self.model).
                filter_by(**filters)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount 

    async def get_one(self, **filters) -> Optional[ModelType]:
        async with self._session_factory() as session:
            session: AsyncSession
            stmt = (
                select(self.model).
                filter_by(**filters)
            )
            row = await session.execute(stmt)
            return row.scalar_one_or_none()

    async def get_multi(
            self,
            order: list[str] = ["id"],
            limit: int = 100,
            offset: int = 0,
    ) -> List[ModelType]:
        async with self._session_factory() as session:
            session: AsyncSession
            stmt = (
                select(self.model).
                order_by(*order).
                limit(limit).
                offset(offset)
            )
            row = await session.execute(stmt)
            return row.scalars().all()
