from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from punq import Container

from application.api.v1.users.schemas import UserCreateSchema, UserDetailSchema
from domain.commands.users import CreateUserCommand, UpdateUserPhotoCommand, DeleteUserCommand
from infrastructure.auth.jwt import verify_token, extract_user_id
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.storages.s3.base import BaseS3Client
from settings.config import Settings
from settings.container import initialize_container
from service.message_bus import MessageBus


router = APIRouter(tags=['Users'], prefix='/users')

security = HTTPBearer()

async def get_current_user_id(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UUID:
    return extract_user_id(verify_token(token.credentials))


class ImageFormat(Enum):
    png = 'image/png'
    jpeg = 'image/jpeg'


@router.post('/')
async def create_user(
    schema: UserCreateSchema,
    container: Annotated[Container, Depends(initialize_container)],
) -> str:
    bus: MessageBus = container.resolve(MessageBus)
    await bus.handle(message=CreateUserCommand(schema.to_user_with_credentials_entity()))
    return 'Thank You! We\'ve send confirmation letter to your email.'


@router.get('/me')
async def get_current_user(
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
    container: Annotated[Container, Depends(initialize_container)],
) -> UserDetailSchema:
    repo: BaseUserRepository = container.resolve(BaseUserRepository)
    user = await repo.get(current_user_id)
    return UserDetailSchema.from_user_entity(user)


@router.delete('/me')
async def delete_current_user(
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
    container: Annotated[Container, Depends(initialize_container)],
) -> str:
    bus: MessageBus = container.resolve(MessageBus)
    await bus.handle(message=DeleteUserCommand(user_id=current_user_id))
    return 'User deleted successfully!'


@router.get('/me/photo/download-url')
async def get_photo_download_url(
        current_user_id: Annotated[UUID, Depends(get_current_user_id)],
        container: Annotated[Container, Depends(initialize_container)],
        content_type: ImageFormat = ImageFormat.png,
) -> dict:
    s3_client: BaseS3Client = container.resolve(BaseS3Client)
    repo: BaseUserRepository = container.resolve(BaseUserRepository)
    user = await repo.get(current_user_id)
    key = user.photo
    download_url = await s3_client.generate_presigned_download_url(
        key=key,
        content_type=content_type.value,
    )
    return {'url': download_url}


@router.post('/me/photo/upload-post')
async def get_photo_upload_post(
        current_user_id: Annotated[UUID, Depends(get_current_user_id)],
        container: Annotated[Container, Depends(initialize_container)],
        content_type: ImageFormat = ImageFormat.png,
) -> dict:
    s3_client: BaseS3Client = container.resolve(BaseS3Client)
    settings: Settings = container.resolve(Settings)
    key = f'{settings.USER_SERVICE_MEDIA_PATH}/user-photos/{current_user_id}/profile-photo.jpg'
    upload_data = await s3_client.generate_presigned_upload_post(
        key=key,
        content_type=content_type.value,
    )
    return upload_data


@router.put('/me/photo/')
async def update_photo_path(
        current_user_id: Annotated[UUID, Depends(get_current_user_id)],
        container: Annotated[Container, Depends(initialize_container)],
        photo_path: str,
) -> str:
    bus: MessageBus = container.resolve(MessageBus)
    await bus.handle(message=UpdateUserPhotoCommand(user_id=current_user_id, photo=photo_path))
    return 'Photo updated successfully!'


@router.get('/{user_id}')
async def get_user(
    user_id: UUID,
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
    container: Annotated[Container, Depends(initialize_container)],
) -> UserDetailSchema:
    # if current_user_id not in settings.ADMINS_IDS:
    #     raise HTTPException()
    return await get_current_user(user_id, container)


@router.delete('/{user_id}')
async def delete_user(
    user_id: UUID,
    current_user_id: Annotated[UUID, Depends(get_current_user_id)],
    container: Annotated[Container, Depends(initialize_container)],
) -> str:
    # if current_user_id not in settings.ADMINS_IDS:
    #     raise HTTPException()
    return await delete_current_user(user_id, container)
