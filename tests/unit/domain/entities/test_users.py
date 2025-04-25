from contextlib import nullcontext as not_raises
from uuid import UUID

import pytest

from domain.entities.users import UserEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO


@pytest.mark.parametrize(
    'user1, user2, expectation',
    [
        (UserEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            email=EmailVO('example@email.com'),
            phone_number=PhoneNumberVO('+12345678910'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ), UserEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            email=EmailVO('example@email.com'),
            phone_number=PhoneNumberVO('+12345678910'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ), not_raises()),
        (UserEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            email=EmailVO('example@email.com'),
            phone_number=PhoneNumberVO('+12345678910'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ), UserEntity(
            id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            email=EmailVO('different@email.com'),
            phone_number=PhoneNumberVO('+01987654321'),
            first_name=NameVO('Doe'),
            last_name=NameVO('Jane'),
            middle_name=NameVO('Middle'),
        ), not_raises()),
        (UserEntity(
            email=EmailVO('example@email.com'),
            phone_number=PhoneNumberVO('+12345678910'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ), UserEntity(
            email=EmailVO('example@email.com'),
            phone_number=PhoneNumberVO('+12345678910'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ), pytest.raises(AssertionError)),
    ]
)
def test_user_entity(user1, user2, expectation):
    with expectation:
        assert user1 == user2