from dataclasses import dataclass
from uuid import UUID

from domain.commands.base import BaseCommand
from domain.entities.users import UserWithCredentialsEntity, UserCredentialsStatus
from domain.value_objects.users import NameVO, EmailVO, PhoneNumberVO


@dataclass
class CreateUserCommand(BaseCommand):
    user_with_credentials: UserWithCredentialsEntity


@dataclass
class DeleteUserCommand(BaseCommand):
    user_id: UUID


@dataclass
class UpdateUserCommand(BaseCommand):
    user_id: UUID
    first_name: NameVO | None = None
    last_name: NameVO | None = None
    middle_name: NameVO | None = None


@dataclass
class UpdateUserEmailCommand(BaseCommand):
    user_id: UUID
    new_email: EmailVO


@dataclass
class UpdateUserPhoneNumberCommand(BaseCommand):
    user_id: UUID
    new_phone_number: PhoneNumberVO


@dataclass
class UpdateUserCredentialsStatusCommand(BaseCommand):
    user_id: UUID
    status: UserCredentialsStatus


@dataclass
class UpdateUserPhotoCommand(BaseCommand):
    user_id: UUID
    photo: str
