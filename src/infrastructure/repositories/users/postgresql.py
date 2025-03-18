from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.users import UserEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO
from infrastructure.converters.users import convert_user_entity_to_model
from infrastructure.models.users import UserModel
from infrastructure.repositories.users.base import BaseUserRepository


@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get(self, user_id: UUID) -> UserEntity | None:
        user = await self.session.get(UserModel, user_id)

        if user:
            return UserEntity(
                id=user.id,
                email=EmailVO(user.email),
                phone_number=PhoneNumberVO(user.phone_number) if user.phone_number else None,
                first_name=NameVO(user.first_name) if user.first_name else None,
                last_name=NameVO(user.last_name) if user.last_name else None,
                middle_name=NameVO(user.middle_name) if user.middle_name else None,
            )


    async def add(self, user: UserEntity) -> None:
        user = convert_user_entity_to_model(user)
        self.session.add(user)
