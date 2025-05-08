from dataclasses import dataclass
from uuid import UUID

from domain.commands.base import BaseCommand
from domain.entities.users import UserWithCredentialsEntity, UserCredentialsStatus


@dataclass
class CreateUserCommand(BaseCommand):
    user_with_credentials: UserWithCredentialsEntity


@dataclass
class UpdateUserCredentialsStatusCommand(BaseCommand):
    user_id: UUID
    status: UserCredentialsStatus


@dataclass
class UpdateUserPhotoCommand(BaseCommand):
    user_id: UUID
    photo: str
