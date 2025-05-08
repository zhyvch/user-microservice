from dataclasses import dataclass, field
from enum import Enum

from domain.entities.base import BaseEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO, PasswordVO


class UserCredentialsStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


@dataclass(eq=False)
class UserEntity(BaseEntity):
    photo: str = field(default='', kw_only=True)
    email: EmailVO
    phone_number: PhoneNumberVO | None
    first_name: NameVO | None
    last_name: NameVO | None
    middle_name: NameVO | None
    credentials_status: UserCredentialsStatus = field(default=UserCredentialsStatus.PENDING, kw_only=True)


@dataclass
class UserWithCredentialsEntity:
    user: UserEntity
    password: PasswordVO
