from contextlib import nullcontext as not_raises
from uuid import uuid4, UUID

import pytest

from application.external_events.handlers.users import UserCredentialsCreatedExternalEventHandler
from domain.entities.users import UserCredentialsStatus
from settings.config import settings
from settings.container import get_commands_map, get_events_map, get_external_events_map


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
            self, random_user_entity, fake_user_uow, fake_consumer, fake_message_bus, body, expectation
    ):
        random_user_entity.id = UUID(body['user_id'])
        async with fake_user_uow:
            await fake_user_uow.users.add(random_user_entity)
            await fake_user_uow.commit()

        handler = UserCredentialsCreatedExternalEventHandler(bus=fake_message_bus)
        async with fake_consumer:
            with expectation:
                await handler(body=body)

                async with fake_user_uow:
                    user = await fake_user_uow.users.get(user_id=random_user_entity.id)
                    assert user.credentials_status == UserCredentialsStatus(body['status'])

        while not fake_consumer.broker.queue.empty():
            expected_produced_topics = ['user.registration.completed']
            item = await fake_consumer.broker.queue.get()
            assert item['topic'] in expected_produced_topics

