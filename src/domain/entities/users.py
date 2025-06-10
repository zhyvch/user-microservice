from dataclasses import dataclass, field
from enum import Enum

from domain.entities.base import BaseEntity
from domain.exceptions.users import InsufficientCredentialsInfoException
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO, PasswordVO


class UserCredentialsStatus(Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


@dataclass(eq=False)
class UserEntity(BaseEntity):
    photo: str = field(default='', kw_only=True)
    email: EmailVO | None
    phone_number: PhoneNumberVO | None
    first_name: NameVO | None
    last_name: NameVO | None
    middle_name: NameVO | None
    credentials_status: UserCredentialsStatus = field(default=UserCredentialsStatus.PENDING, kw_only=True)

    def __post_init__(self):
        if not any([self.email, self.phone_number]):
            raise InsufficientCredentialsInfoException


@dataclass
class UserWithCredentialsEntity:
    user: UserEntity
    password: PasswordVO
