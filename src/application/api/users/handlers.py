from uuid import UUID

from fastapi import APIRouter

from application.api.users.schemas import (
    UserCreateSchema,
    UserDetailSchema,
    UserUpdateSchema,
)
from service.services import create_user_use_case, get_user_use_case, update_user_use_case, delete_user_use_case
from service.units_of_work.users.postgresql import SQLAlchemyUserUnitOfWork

router = APIRouter(tags=['Users'])

@router.post('/')
async def create_user(
    schema: UserCreateSchema,
) -> UserDetailSchema:
    ...

@router.get('/{user_id}')
async def get_user(
    user_id: UUID,
) -> UserDetailSchema:
    ...

@router.patch('/{user_id}')
async def update_user(
    user_id: UUID,
    schema: UserUpdateSchema,
) -> UserDetailSchema:
    ...

@router.delete('/{user_id}')
async def delete_user(
    user_id: UUID,
) -> ...:
    ...

# @router.patch('/{user_id}/credentials') ?
# async def update_credentials(
#     user_id: UUID,
#     schema: UserUpdateCredentialsSchema,
# ) -> UserDetailSchema:
#     ...