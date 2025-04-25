from contextlib import nullcontext as not_raises

import pytest

from domain.exceptions.users import (
    PasswordTypeException,
    PasswordIsEmptyException,
    PasswordTooShortException,
    PasswordTooLongException,
    PasswordNotContainingDigitsException,
    PasswordNotContainingCapitalLetterException,
    PasswordNotContainingSpecialSymbolException,
)
from domain.value_objects.users import PasswordVO


@pytest.mark.parametrize(
    'passwords, expectation',
    [
        (['Very$ecurePa$$word31012007'], not_raises()),
        ([100, 12.3, True, None, [], {}, ()], pytest.raises(PasswordTypeException)),
        ([''], pytest.raises(PasswordIsEmptyException)),
        (['Ve7¥secur'], pytest.raises(PasswordTooShortException)),
        (['Very$ecurePa$$word31012007' * 100], pytest.raises(PasswordTooLongException)),
        (['Very$ecurePa$$word'], pytest.raises(PasswordNotContainingDigitsException)),
        (['very$ecurepa$$word31012007'], pytest.raises(PasswordNotContainingCapitalLetterException)),
        (['VerySecurePaSSword31012007'], pytest.raises(PasswordNotContainingSpecialSymbolException)),
    ]
)
def test_phone_number_vo_inputs(passwords, expectation):
    with expectation:
        for password in passwords:
            PasswordVO(password)


@pytest.mark.parametrize(
    'password1, password2, expectation',
    [
        ('Very$ecurePa$$word31012007', 'Very$ecurePa$$word31012007', not_raises()),
        ('Very$ecurePa$$word31012007', '31012007Pa$$word$ecureVery', pytest.raises(AssertionError)),
    ]
)
def test_password_vos_equality(password1, password2, expectation):
    with expectation:
        assert PasswordVO(password1) == PasswordVO(password2)
