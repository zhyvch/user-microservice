from contextlib import nullcontext as not_raises
from datetime import datetime
from uuid import UUID

import pytest

from domain.entities.users import UserCredentialsStatus
from domain.events.users import (
    UserCreatedEvent,
    UserDeletedEvent,
    UserRegistrationCompletedEvent,
)

now = datetime.now()


@pytest.mark.parametrize(
    'event1, event2, expectation',
    [
        (UserCreatedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
        ), UserCreatedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
        ), not_raises()),
        (UserCreatedEvent(
            event_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
        ), UserCreatedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            password='<PASSWORD>',
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
        ), pytest.raises(AssertionError)),

    ]
)
def test_user_created_events(event1, event2, expectation):
    with expectation:
        assert event1 == event2


@pytest.mark.parametrize(
    'event1, event2, expectation',
    [
        (UserDeletedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
        ), UserDeletedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
        ), not_raises()),
        (UserDeletedEvent(
            event_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
        ), UserDeletedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
        ), pytest.raises(AssertionError)),
    ]
)
def test_user_deleted_events(event1, event2, expectation):
    with expectation:
        assert event1 == event2


@pytest.mark.parametrize(
    'event1, event2, expectation',
    [
        (UserRegistrationCompletedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            photo='<PHOTO>',
            created_at=now,
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
            first_name='<FIRST_NAME>',
            last_name='<LAST_NAME>',
            middle_name='<MIDDLE_NAME>',
            credentials_status=UserCredentialsStatus.SUCCESS,
        ), UserRegistrationCompletedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            photo='<PHOTO>',
            created_at=now,
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
            first_name='<FIRST_NAME>',
            last_name='<LAST_NAME>',
            middle_name='<MIDDLE_NAME>',
            credentials_status=UserCredentialsStatus.SUCCESS,
        ), not_raises()),
        (UserRegistrationCompletedEvent(
            event_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            photo='<PHOTO>',
            created_at=now,
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
            first_name='<FIRST_NAME>',
            last_name='<LAST_NAME>',
            middle_name='<MIDDLE_NAME>',
            credentials_status=UserCredentialsStatus.SUCCESS,
        ), UserRegistrationCompletedEvent(
            event_id=UUID('0e6315a5-7980-4a14-a902-29a428054c8a'),
            user_id=UUID('5dcac3ad-330b-4d53-b59f-cb3a3b48a985'),
            photo='<PHOTO>',
            created_at=now,
            email='<EMAIL>',
            phone_number='<PHONE_NUMBER>',
            first_name='<FIRST_NAME>',
            last_name='<LAST_NAME>',
            middle_name='<MIDDLE_NAME>',
            credentials_status=UserCredentialsStatus.SUCCESS,
        ), pytest.raises(AssertionError)),
    ]
)
def test_user_registration_completed_events(event1, event2, expectation):
    with expectation:
        assert event1 == event2
