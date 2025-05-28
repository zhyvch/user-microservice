import asyncio
from contextlib import nullcontext as not_raises
from uuid import uuid4, UUID

import pytest
import orjson

from application.external_events.handlers.users import UserCredentialsCreatedExternalEventHandler
from domain.entities.users import UserCredentialsStatus
from settings.container import get_external_events_map


@pytest.mark.asyncio
class TestExternalEventHandlers:
    @pytest.mark.parametrize(
        'body, expectation',
        [
            ({'user_id': str(uuid4()), 'status': UserCredentialsStatus.SUCCESS.value}, not_raises()),
            ({'user_id': str(uuid4()), 'status': UserCredentialsStatus.FAILED.value}, not_raises()),
            ({'user_id': str(uuid4()), 'status': UserCredentialsStatus.PENDING.value}, not_raises()),
        ],
    )
    async def test_user_credentials_created_external_event_handler(
            self, random_user_entity, sqlalchemy_user_uow, rabbitmq_consumer, message_bus, body, expectation
    ):
        queue = await rabbitmq_consumer.channel.declare_queue(
            name="",
            durable=False,
            exclusive=True,
            auto_delete=True
        )
        await queue.bind(rabbitmq_consumer.exchange, 'user.registration.completed')
        random_user_entity.id = UUID(body['user_id'])
        async with sqlalchemy_user_uow:
            await sqlalchemy_user_uow.users.add(random_user_entity)
            await sqlalchemy_user_uow.commit()

        message_bus.uow = sqlalchemy_user_uow
        rabbitmq_consumer.external_events_map = get_external_events_map(bus=message_bus) # we dont restart because external_events_map only used on consumption

        handler = UserCredentialsCreatedExternalEventHandler(bus=message_bus)
        with expectation:
            await handler(body)

        async with sqlalchemy_user_uow:
            user = await sqlalchemy_user_uow.users.get(body['user_id'])
            assert user is not None
            assert user == random_user_entity
            assert user.credentials_status.value == body['status']

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
