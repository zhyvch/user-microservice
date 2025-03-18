from uuid import UUID

from domain.entities.users import UserEntity
from infrastructure.repositories.users.base import BaseUserRepository
from service.units_of_work.users.base import BaseUserUnitOfWork

# TODO: some "middleware" to auth jwt perhaps in application layer
# TODO: class-wrap services/use_cases; also CQRS i guess


async def create_user_use_case(user: UserEntity, uow: BaseUserUnitOfWork) -> None:
    async with uow:
        await uow.users.add(user=user)
        # TODO: send creds via broker to auth service
        # TODO: send notification via broker to notification service
        await uow.commit()


async def get_user_use_case(user_id: UUID, uow: BaseUserUnitOfWork) -> UserEntity:
    async with uow:
        user = await uow.users.get(user_id=user_id)
    return user


async def update_user_use_case(user_id: UUID, user: UserEntity, uow: BaseUserUnitOfWork) -> None:
    async with uow:
        # TODO: updating mechanism
        # TODO: send creds if creds to update via broker to auth service
        # TODO: send notification via broker to notification service
        await uow.commit()


async def delete_user_use_case(user_id: UUID, uow: BaseUserUnitOfWork) -> None:
    async with uow:
        # TODO: send event to delete creds via broker to auth service
        # TODO: send notification via broker to notification service
        # await uow.users.remove(user_id=user_id)
        await uow.commit()