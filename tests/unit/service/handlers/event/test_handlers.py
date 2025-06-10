import pytest

from domain.events.users import (
    UserCreatedEvent,
    UserRegistrationCompletedEvent,
    UserDeletedEvent,
)
from service.handlers.event.users import (
    UserCreatedEventHandler,
    UserRegistrationCompletedEventHandler,
    UserDeletedEventHandler,
)


@pytest.mark.asyncio
class TestEventHandlers:
    async def test_user_created_event_handler(
        self, random_user_entity, fake_user_uow, fake_producer
    ):
        event = UserCreatedEvent(
            user_id=random_user_entity.id,
            password='VerySecretPa$$word1234',
            email=random_user_entity.email.as_generic(),
            phone_number=random_user_entity.phone_number.as_generic(),
        )
        handler = UserCreatedEventHandler(producer=fake_producer, topic='user.created')
        await handler(event=event)

        assert fake_producer.broker.queue.pop()['event'] == UserCreatedEvent.__name__


    async def test_user_deleted_event_handler(
        self, random_user_entity, fake_user_uow, fake_producer
    ):
        event = UserDeletedEvent(
            user_id=random_user_entity.id,
        )
        handler = UserDeletedEventHandler(producer=fake_producer, topic='user.deleted')
        await handler(event=event)

        assert fake_producer.broker.queue.pop()['event'] == UserDeletedEvent.__name__


    async def test_user_registration_completed_event_handler(
        self, random_user_entity, fake_user_uow, fake_producer
    ):
        event = UserRegistrationCompletedEvent(
            user_id=random_user_entity.id,
            photo=random_user_entity.photo,
            created_at=random_user_entity.created_at,
            email=random_user_entity.email.value,
            phone_number=random_user_entity.phone_number,
            first_name=random_user_entity.first_name.value if random_user_entity.first_name else None,
            last_name=random_user_entity.last_name.value if random_user_entity.last_name else None,
            middle_name=random_user_entity.middle_name.value if random_user_entity.middle_name else None,
            credentials_status=random_user_entity.credentials_status,
        )
        handler = UserRegistrationCompletedEventHandler(producer=fake_producer, topic='user.registration.completed')
        await handler(event=event)

        assert fake_producer.broker.queue.pop()['event'] == UserRegistrationCompletedEvent.__name__
