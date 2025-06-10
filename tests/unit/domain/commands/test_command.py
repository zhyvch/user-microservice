from contextlib import nullcontext as not_raises
from uuid import UUID

import pytest

from domain.commands.users import (
    CreateUserCommand,
    UpdateUserCredentialsStatusCommand,
    UserCredentialsStatus,
    DeleteUserCommand,
    UpdateUserCommand,
    UpdateUserEmailCommand,
    UpdateUserPhoneNumberCommand,
    UpdateUserPhotoCommand,
)
from domain.entities.users import UserWithCredentialsEntity, UserEntity
from domain.value_objects.users import PasswordVO, EmailVO, PhoneNumberVO, NameVO


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (CreateUserCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_with_credentials=UserWithCredentialsEntity(
                UserEntity(
                    id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
                    email=EmailVO('example@email.com'),
                    phone_number=PhoneNumberVO('+12345678910'),
                    first_name=NameVO('John'),
                    last_name=NameVO('Doe'),
                    middle_name=None,
                ),
                PasswordVO('Very$$ecurePassword123'),
            ),
        ),
        CreateUserCommand(
             command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
             user_with_credentials=UserWithCredentialsEntity(
                 UserEntity(
                     id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
                     email=EmailVO('example@email.com'),
                     phone_number=PhoneNumberVO('+12345678910'),
                     first_name=NameVO('John'),
                     last_name=NameVO('Doe'),
                     middle_name=None,
                 ),
                 PasswordVO('Very$$ecurePassword123'),
             ),
         ),
         not_raises()),
        (CreateUserCommand(
            user_with_credentials=UserWithCredentialsEntity(
                UserEntity(
                    id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
                    email=EmailVO('example@email.com'),
                    phone_number=PhoneNumberVO('+12345678910'),
                    first_name=NameVO('John'),
                    last_name=NameVO('Doe'),
                    middle_name=None,
                ),
                PasswordVO('Very$$ecurePassword123'),
            ),
         ),
         CreateUserCommand(
             user_with_credentials=UserWithCredentialsEntity(
                 UserEntity(
                     id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
                     email=EmailVO('example@email.com'),
                     phone_number=PhoneNumberVO('+12345678910'),
                     first_name=NameVO('John'),
                     last_name=NameVO('Doe'),
                     middle_name=None,
                 ),
                 PasswordVO('Very$$ecurePassword123'),
             ),
         ),
         pytest.raises(AssertionError)),
    ]
)
def test_create_user_command(command1, command2, expectation):
    with expectation:
        assert command1 == command2


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (UpdateUserCredentialsStatusCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            status=UserCredentialsStatus.SUCCESS,
        ),
         UpdateUserCredentialsStatusCommand(
             command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
             status=UserCredentialsStatus.SUCCESS,
         ),
         not_raises()),
        (UpdateUserCredentialsStatusCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            status=UserCredentialsStatus.FAILED,
        ),
         UpdateUserCredentialsStatusCommand(
             command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
             status=UserCredentialsStatus.SUCCESS,
         ),
         pytest.raises(AssertionError)),
        (UpdateUserCredentialsStatusCommand(
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            status=UserCredentialsStatus.SUCCESS,
        ),
         UpdateUserCredentialsStatusCommand(
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
             status=UserCredentialsStatus.SUCCESS,
         ),
         pytest.raises(AssertionError)),
    ]
)
def test_update_user_creds_status_command(command1, command2, expectation):
    with expectation:
        assert command1 == command2


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (DeleteUserCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
        ),
         DeleteUserCommand(
             command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
         ),
         not_raises()),
        (DeleteUserCommand(
            command_id=UUID('0e6315a5-1000-0000-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
        ),
         DeleteUserCommand(
             command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8b'),
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
         ),
         pytest.raises(AssertionError)),
    ]
)
def test_delete_user_command_equality(command1, command2, expectation):
    with expectation:
        assert command1 == command2


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (UpdateUserCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ),
         UpdateUserCommand(
             command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
             first_name=NameVO('John'),
             last_name=NameVO('Doe'),
             middle_name=None,
         ),
         not_raises()),
        (UpdateUserCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            first_name=NameVO('John'),
            last_name=NameVO('Doe'),
            middle_name=None,
        ),
         UpdateUserCommand(
             command_id=UUID('0e6315a5-1000-0000-a902-29a428054c8b'),
             user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
             first_name=NameVO('John'),
             last_name=NameVO('Doe'),
             middle_name=None,
         ),
         pytest.raises(AssertionError)),
    ]
)
def test_update_user_command(command1, command2, expectation):
    with expectation:
        assert command1 == command2


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (UpdateUserEmailCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_email=EmailVO('test@testmail.com'),
        ),
        UpdateUserEmailCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_email=EmailVO('test@testmail.com'),
        ),
        not_raises()),
        (UpdateUserEmailCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_email=EmailVO('test@testmail.com'),
        ),
        UpdateUserEmailCommand(
            command_id=UUID('0e6315a5-1000-0000-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_email=EmailVO('test@testmail.com'),
        ),
        pytest.raises(AssertionError)),
    ]
)
def test_update_user_email_command(command1, command2, expectation):
    with expectation:
        assert command1 == command2


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (UpdateUserPhoneNumberCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_phone_number=PhoneNumberVO('+12345678910'),
        ),
        UpdateUserPhoneNumberCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_phone_number=PhoneNumberVO('+12345678910'),
        ),
        not_raises()),
        (UpdateUserPhoneNumberCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_phone_number=PhoneNumberVO('+12345678910'),
        ),
        UpdateUserPhoneNumberCommand(
            command_id=UUID('0e6315a5-1000-0000-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            new_phone_number=PhoneNumberVO('+12345678910'),
        ),
        pytest.raises(AssertionError)),
    ]
)
def test_update_user_phone_number_command(command1, command2, expectation):
    with expectation:
        assert command1 == command2


@pytest.mark.parametrize(
    'command1, command2, expectation',
    [
        (UpdateUserPhotoCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            photo='base64_encoded_photo_string',
        ),
        UpdateUserPhotoCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8a'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            photo='base64_encoded_photo_string',
        ),
        not_raises()),
        (UpdateUserPhotoCommand(
            command_id=UUID('0e6315a5-1000-4a14-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            photo='base64_encoded_photo_string',
        ),
        UpdateUserPhotoCommand(
            command_id=UUID('0e6315a5-1000-0000-a902-29a428054c8b'),
            user_id=UUID('9e9a9d70-81cb-4d9a-829f-1a6069a97d88'),
            photo='base64_encoded_photo_string',
        ),
        pytest.raises(AssertionError)),
    ]
)
def test_update_user_photo_command(command1, command2, expectation):
    with expectation:
        assert command1 == command2
