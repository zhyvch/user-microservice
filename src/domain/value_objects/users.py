from dataclasses import dataclass

from domain.exceptions.users import (
    EmailTypeException,
    EmailIsEmptyException,
    EmailTooShortException,
    EmailTooLongException,
    EmailNotContainingAtSymbolException,
    PhoneNumberTypeException,
    PhoneNumberIsEmptyException,
    PhoneNumberTooShortException,
    PhoneNumberTooLongException,
    PhoneNumberNotStartingWithPlusSymbolException,
    PhoneNumberContainsNonDigitsException,
    NameTypeException,
    NameIsEmptyException,
    NameTooLongException,
    PasswordTypeException,
    PasswordIsEmptyException,
    PasswordTooShortException,
    PasswordTooLongException,
    PasswordNotContainingDigitsException,
    PasswordNotContainingCapitalLetterException,
    PasswordNotContainingSpecialSymbolException,
)
from domain.value_objects.base import BaseVO

# TODO: Move validation to a separate class

@dataclass(frozen=True)
class EmailVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not isinstance(self.value, str):
            raise EmailTypeException()

        if not self.value:
            raise EmailIsEmptyException()

        if len(self.value) < 6:
            raise EmailTooShortException(self.value)

        if len(self.value) > 255:
            raise EmailTooLongException(self.value)

        if '@' not in self.value:
            raise EmailNotContainingAtSymbolException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PhoneNumberVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not isinstance(self.value, str):
            raise PhoneNumberTypeException()

        if not self.value:
            raise PhoneNumberIsEmptyException()

        if len(self.value) < 7:
            raise PhoneNumberTooShortException(self.value)

        if len(self.value) > 15:
            raise PhoneNumberTooLongException(self.value)

        if not self.value.startswith('+'):
            raise PhoneNumberNotStartingWithPlusSymbolException(self.value)

        if not self.value[1:].isdecimal():
            raise PhoneNumberContainsNonDigitsException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class NameVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not isinstance(self.value, str):
            raise NameTypeException()

        if not self.value:
            raise NameIsEmptyException()

        if len(self.value) > 255:
            raise NameTooLongException(self.value)

        return True

    def as_generic(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class PasswordVO(BaseVO):
    value: str

    def validate(self) -> bool:
        if not isinstance(self.value, str):
            raise PasswordTypeException()

        if not self.value:
            raise PasswordIsEmptyException()

        if len(self.value) < 10:
            raise PasswordTooShortException()

        if len(self.value) > 255:
            raise PasswordTooLongException()

        if not any(char.isdigit() for char in self.value):
            raise PasswordNotContainingDigitsException()

        if not any(char.isupper() for char in self.value):
            raise PasswordNotContainingCapitalLetterException()

        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~`' for char in self.value):
            raise PasswordNotContainingSpecialSymbolException()

        return True

    def as_generic(self) -> str:
        return str(self.value)