from typing import Annotated

from fastapi import APIRouter, Depends
from punq import Container

from application.api.users.schemas import (
    UserCreateSchema,
)
from domain.commands.users import UserCreateCommand
from service.container import initialize_container
from service.message_bus import MessageBus

router = APIRouter(tags=['Users'])


@router.post('/')
async def create_user(
    schema: UserCreateSchema,
    container: Annotated[Container, Depends(initialize_container)]
) -> str:
    bus: MessageBus = container.resolve(MessageBus)
    await bus.handle(message=UserCreateCommand(schema.to_user_with_credentials()))

    return 'User successfully created'
