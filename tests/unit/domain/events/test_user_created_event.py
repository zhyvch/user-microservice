from contextlib import nullcontext as not_raises
from uuid import UUID

import pytest

from domain.events.users import UserCreatedEvent


@pytest.mark.parametrize(
    'event1, event2, expectation',
    [
        (UserCreatedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
        ), UserCreatedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
        ), not_raises()),
        (UserCreatedEvent(
            event_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
        ), UserCreatedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
        ), pytest.raises(AssertionError)),

    ]
)
def test_user_created_events(event1, event2, expectation):
    with expectation:
        assert event1 == event2