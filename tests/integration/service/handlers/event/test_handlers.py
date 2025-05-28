import pytest
from orjson import orjson

from domain.events.users import UserCreatedEvent, UserDeletedEvent, UserRegistrationCompletedEvent
from service.handlers.event.users import UserCreatedEventHandler, UserDeletedEventHandler, \
    UserRegistrationCompletedEventHandler
from settings.container import get_external_events_map



@pytest.mark.asyncio
class TestEventHandlers:
    async def test_user_created_event_handler(
        self, random_user_entity, sqlalchemy_user_uow, rabbitmq_producer, rabbitmq_consumer, message_bus
    ):
        queue = await rabbitmq_consumer.channel.declare_queue(
            name="",
            durable=False,
            exclusive=True,
            auto_delete=True
        )
        await queue.bind(rabbitmq_consumer.exchange, 'user.created')
        message_bus.uow = sqlalchemy_user_uow
        rabbitmq_consumer.external_events_map = get_external_events_map(bus=message_bus)  # we dont restart because external_events_map only used on consumption

        event = UserCreatedEvent(
            user_id=random_user_entity.id,
            password='VerySecretPa$$word1234',
            email=random_user_entity.email.value,
        )
        handler = UserCreatedEventHandler(producer=rabbitmq_producer, topic='user.created')
        await handler(event=event)

        messages = []
        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    messages.append(message)
                    if queue_iterator._queue.empty():
                        break

        assert len(messages) == 1
        consumed_message = orjson.loads(messages[0].body)
        assert consumed_message['user_id'] == str(random_user_entity.id)

    async def test_user_deleted_event_handler(
        self, random_user_entity, sqlalchemy_user_uow, rabbitmq_producer, rabbitmq_consumer, message_bus
    ):
        queue = await rabbitmq_consumer.channel.declare_queue(
            name="",
            durable=False,
            exclusive=True,
            auto_delete=True
        )
        await queue.bind(rabbitmq_consumer.exchange, 'user.deleted')
        message_bus.uow = sqlalchemy_user_uow
        rabbitmq_consumer.external_events_map = get_external_events_map(bus=message_bus)  # we dont restart because external_events_map only used on consumption

        event = UserDeletedEvent(
            user_id=random_user_entity.id,
        )
        handler = UserDeletedEventHandler(producer=rabbitmq_producer, topic='user.deleted')
        await handler(event=event)

        messages = []
        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    messages.append(message)
                    if queue_iterator._queue.empty():
                        break

        assert len(messages) == 1
        consumed_message = orjson.loads(messages[0].body)
        assert consumed_message['user_id'] == str(random_user_entity.id)


    async def test_user_registration_completed_event_handler(
        self, random_user_entity, sqlalchemy_user_uow, rabbitmq_producer, rabbitmq_consumer, message_bus
    ):
        queue = await rabbitmq_consumer.channel.declare_queue(
            name="",
            durable=False,
            exclusive=True,
            auto_delete=True
        )
        await queue.bind(rabbitmq_consumer.exchange, 'user.registration.completed')
        message_bus.uow = sqlalchemy_user_uow
        rabbitmq_consumer.external_events_map = get_external_events_map(bus=message_bus)  # we dont restart because external_events_map only used on consumption

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
        handler = UserRegistrationCompletedEventHandler(producer=rabbitmq_producer, topic='user.registration.completed')
        await handler(event=event)

        messages = []
        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    messages.append(message)
                    if queue_iterator._queue.empty():
                        break

        assert len(messages) == 1
        consumed_message = orjson.loads(messages[0].body)
        assert consumed_message['user_id'] == str(random_user_entity.id)
