from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class EmailTypeException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Email should be a string type'


@dataclass(frozen=True, eq=False)
class EmailIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Email is empty'


@dataclass(frozen=True, eq=False)
class EmailTooShortException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> is too short'


@dataclass(frozen=True, eq=False)
class EmailTooLongException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email[255:]}...> is too long'


@dataclass(frozen=True, eq=False)
class EmailNotContainingAtSymbolException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f'Email <{self.email}> must contain an "@" symbol'


@dataclass(frozen=True, eq=False)
class PhoneNumberTypeException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Phone number should be a string type'


@dataclass(frozen=True, eq=False)
class PhoneNumberIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Phone number is empty'


@dataclass(frozen=True, eq=False)
class PhoneNumberTooShortException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number[15:]}...> is too short'


@dataclass(frozen=True, eq=False)
class PhoneNumberTooLongException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number[15:]}...> is too long'


@dataclass(frozen=True, eq=False)
class PhoneNumberNotStartingWithPlusSymbolException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number}> must start with "+" symbol'


@dataclass(frozen=True, eq=False)
class PhoneNumberContainsNonDigitsException(ApplicationException):
    phone_number: str

    @property
    def message(self) -> str:
        return f'Phone number <{self.phone_number}> must contain only digits'


@dataclass(frozen=True, eq=False)
class NameTypeException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Name should be a string type'


@dataclass(frozen=True, eq=False)
class NameIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Name is empty'


@dataclass(frozen=True, eq=False)
class NameTooLongException(ApplicationException):
    name: str

    @property
    def message(self) -> str:
        return f'Name <{self.name[255:]}...> is too long'


@dataclass(frozen=True, eq=False)
class PasswordTypeException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password should be a string type'


@dataclass(frozen=True, eq=False)
class PasswordIsEmptyException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password is empty'


@dataclass(frozen=True, eq=False)
class PasswordTooShortException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password is too short'


@dataclass(frozen=True, eq=False)
class PasswordTooLongException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password is too long'


@dataclass(frozen=True, eq=False)
class PasswordNotContainingDigitsException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password must contain at least one digit'


@dataclass(frozen=True, eq=False)
class PasswordNotContainingCapitalLetterException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password must contain at least one capital letter'


@dataclass(frozen=True, eq=False)
class PasswordNotContainingSpecialSymbolException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Password must contain at least special symbol (e.g. !@#$%^&*()-_=+[]{}|;:,.<>?/~` )'
