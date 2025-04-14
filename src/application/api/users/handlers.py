from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from punq import Container

from application.api.users.schemas import UserCreateSchema, UserDetailSchema
from domain.commands.users import CreateUserCommand
from infrastructure.auth.jwt import verify_token, extract_user_id
from infrastructure.repositories.users.base import BaseUserRepository
from settings.container import initialize_container
from service.message_bus import MessageBus

router = APIRouter(tags=['Users'])

security = HTTPBearer()

async def get_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict[str, Any]:
    return verify_token(credentials.credentials)

async def get_current_user_id(
    payload: Annotated[dict[str, Any], Depends(get_token_payload)]
) -> UUID:
    return extract_user_id(payload)


@router.post('/')
async def create_user(
    schema: UserCreateSchema,
    container: Annotated[Container, Depends(initialize_container)],
) -> str:
    bus: MessageBus = container.resolve(MessageBus)
    await bus.handle(message=CreateUserCommand(schema.to_user_with_credentials()))
    return 'User successfully created'


@router.get('/me')
async def get_current_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    container: Annotated[Container, Depends(initialize_container)],
) -> UserDetailSchema:
    repo = container.resolve(BaseUserRepository)
    user = await repo.get(user_id)
    return UserDetailSchema(
        id=user.id,
        created_at=user.created_at,
        email=user.email.as_generic(),
        phone_number=user.phone_number.as_generic() if user.phone_number else None,
        first_name=user.first_name.as_generic() if user.first_name else None,
        last_name=user.last_name.as_generic() if user.last_name else None,
        middle_name=user.middle_name.as_generic() if user.middle_name else None,
    )
