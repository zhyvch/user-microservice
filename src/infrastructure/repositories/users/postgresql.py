from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserEntity
from infrastructure.converters.users import convert_user_entity_to_model, convert_user_model_to_entity
from infrastructure.models.users import UserModel
from infrastructure.repositories.users.base import BaseUserRepository


@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get(self, user_id: UUID) -> UserEntity | None:
        user = await self.session.get(UserModel, user_id)

        if user:
            user = convert_user_model_to_entity(user)
            return user


    async def add(self, user: UserEntity) -> None:
        print(f'In repository {user.id}')
        user = convert_user_entity_to_model(user)
        print(f'Out repository {user.id}')
        self.session.add(user)

