from typing import Generic, TypeVar
from src.schemas.base_schema import CreateSchemaType, UpdateSchemaType
from src.repositories.base_repository import AbstractRepository
from src.models.base_model import ModelType

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
            self, 
            repository: AbstractRepository
    )->None:
        self.repository = repository

    async def create(self, model: CreateSchemaType) -> ModelType:
        return await self.repository.create(data=model.model_dump())

    async def update(self, pk:int, model: UpdateSchemaType) -> ModelType:
        return await self.repository.update(data=model.model_dump(), id=pk) 

    async def delete(self, pk:int) -> ModelType:
        await self.repository.delete(id=pk)
    
    async def get_one(self, pk:int)-> ModelType:
        return await self.repository.get_one(id=pk)