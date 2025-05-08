import pytest

from domain.events.users import UserCreatedEvent, UserRegistrationCompletedEvent
from service.handlers.event.users import UserCreatedEventHandler, UserRegistrationCompletedEventHandler


@pytest.mark.asyncio
class TestEventHandlers:
    async def test_user_created_event_handler(
            self, random_user_entity, fake_user_uow, fake_producer
    ):
        event = UserCreatedEvent(
            user_id=random_user_entity.id,
            password='VerySecretPa$$word1234',
            email=random_user_entity.email.value,
        )
        topic_to_produce = 'user.created'
        handler = UserCreatedEventHandler(producer=fake_producer, topic=topic_to_produce)
        await handler(event=event)

        while not fake_producer.broker.queue.empty():
            expected_produced_topics = [topic_to_produce]
            item = await fake_producer.broker.queue.get()
            assert item['topic'] in expected_produced_topics

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
        topic_to_produce = 'user.registration.completed'
        handler = UserRegistrationCompletedEventHandler(producer=fake_producer, topic=topic_to_produce)
        await handler(event=event)

        while not fake_producer.broker.queue.empty():
            expected_produced_topics = [topic_to_produce]
            item = await fake_producer.broker.queue.get()
            assert item['topic'] in expected_produced_topics
