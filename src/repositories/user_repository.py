from sqlalchemy import select
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.models.user_model import UserTable as UserModel
from src.config.database.db_helper import db_helper
from src.schemas.user_schemas import UserCreate, UserUpdate

class UserRepository(SqlAlchemyRepository[UserModel, UserCreate, UserUpdate]):
    
    async def all(self) -> list[UserModel] | None:
        """
        Получить всех юзеров системы
        """
        async with self._session_factory() as session:
            smtp = select(self.model)
            row = await session.execute(smtp)
            return row.scalars().all()

    async def exists(self, **filters) -> bool:
        """
        Проверка, что пользователь существует
        """
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None

user_repository = UserRepository(
    model=UserModel, 
    db_session=db_helper.get_db_session
)