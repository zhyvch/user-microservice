from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.commands.users import UserCredentialsStatus
from domain.entities.users import UserEntity
from infrastructure.cache import cache_repository
from infrastructure.converters.users import convert_user_entity_to_model, convert_user_model_to_entity
from infrastructure.models.users import UserModel
from infrastructure.repositories.users.base import BaseUserRepository


@cache_repository
@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get(self, user_id: UUID) -> UserEntity | None:
        user = await self.session.get(UserModel, user_id)
        if user:
            user = convert_user_model_to_entity(user)
            return user

    async def add(self, user: UserEntity) -> None:
        user = convert_user_entity_to_model(user)
        self.session.add(user)

    async def update_status(self, user_id: UUID, status: UserCredentialsStatus) -> None:
        user = await self.session.get(UserModel, user_id)
        if user:
            user.credentials_status = status
