import asyncio
import logging
from dataclasses import field, dataclass
from uuid import UUID

from application.external_events.consumers.base import BaseConsumer
from application.external_events.handlers.base import BaseExternalEventHandler
from domain.entities.users import UserEntity, UserCredentialsStatus
from domain.commands.base import BaseCommand
from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer
from infrastructure.repositories.users.base import BaseUserRepository
from service.units_of_work.users.base import BaseUserUnitOfWork


logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class FakeUserRepository(BaseUserRepository):
    users_list: list[UserEntity] = field(default_factory=list)

    async def get(self, user_id: UUID) -> UserEntity | None:
        logger.info('Fetching user with ID: %s', user_id)
        for user in self.users_list:
            if user.id == user_id:
                logger.info('User found: %s', user_id)
                return user
        logger.warning('User not found: %s', user_id)
        return None

    async def remove(self, user_id: UUID) -> None:
        logger.info('Removing user with ID: %s', user_id)
        for user in self.users_list:
            if user.id == user_id:
                self.users_list.remove(user)
                logger.debug('User removed successfully: %s', user_id)
                return None
        logger.warning('Failed to remove user: %s not found', user_id)
        return None

    async def update_status(self, user_id: UUID, status: UserCredentialsStatus) -> None:
        logger.info('Updating status for user %s to %s', user_id, status)
        for user in self.users_list:
            if user_id == user.id:
                user.credentials_status = status
                logger.debug('Status updated successfully for user %s', user_id)
                return None
        logger.warning('Failed to update status: user %s not found', user_id)
        return None

    async def update_photo(self, user_id: UUID, photo: str) -> None:
        logger.info('Updating photo for user %s', user_id)
        for user in self.users_list:
            if user_id == user.id:
                user.photo = photo
                logger.debug('Photo updated successfully for user %s', user_id)
                return None
        logger.warning('Failed to update photo: user %s not found', user_id)
        return None

    async def add(self, user: UserEntity) -> None:
        logger.info('Adding user with ID: %s', user.id)
        self.users_list.append(user)
        return None


class FakeUnitOfWork(BaseUserUnitOfWork):
    def __init__(self):
        logger.debug('Initializing FakeUnitOfWork')
        self.users = FakeUserRepository()
        self.committed = False

    async def commit(self):
        logger.debug('Committing FakeUnitOfWork')
        self.committed = True

    async def rollback(self):
        logger.debug('Rolling back FakeUnitOfWork')
        pass


@dataclass
class FakeBroker(metaclass=SingletonMeta):
    queue: list = field(default_factory=list)


class FakeProducer(BaseProducer):
    broker = FakeBroker()

    async def start(self):
        logger.debug('Starting FakeProducer')
        pass

    async def stop(self):
        logger.debug('Stopping FakeProducer')
        pass

    async def publish(self, event: BaseEvent, topic: str):
        logger.debug('Publishing event to topic: %s', topic)
        self.broker.queue.append({'topic': topic, 'event': event.__class__.__name__, 'body': event.__dict__})


@dataclass
class FakeConsumer(BaseConsumer):
    broker: FakeBroker = field(default_factory=FakeBroker, kw_only=True)
    consuming_task: asyncio.Task | None = field(default=None, kw_only=True)
    topics_to_consume: list[str] = field(default_factory=list, kw_only=True)

    async def start(self):
        logger.debug('Starting FakeConsumer')
        if not self.consuming_task:
            logger.debug('Creating new consuming task')
            self.consuming_task = asyncio.create_task(self.consume())

    async def stop(self):
        logger.debug('Stopping FakeConsumer')
        if self.consuming_task:
            logger.debug('Cancelling consuming task')
            self.consuming_task.cancel()
            self.consuming_task = None

    async def consume(self):
        logger.debug('FakeConsumer consuming messages')
        while True:
            for m in self.broker.queue:
                if m['topic'] in self.topics_to_consume:
                    logger.debug('Processing message for topic: %s', m['topic'])
                    await self.external_events_map[m['topic']](m['body'])
                    self.broker.queue.remove(m)
                else:
                    logger.debug('Ignoring message for topic: %s', m['topic'])
            await asyncio.sleep(0.1)


class FakeCommand(BaseCommand):
    ...


class FakeEvent(BaseEvent):
    ...


class FakeExternalEventHandler(BaseExternalEventHandler):
    body = None

    async def __call__(self, body: dict) -> None:
        self.body = body
        logger.info('FakeExternalEventHandler called with body: %s', body)


def get_fake_external_events_map() -> dict[str, BaseExternalEventHandler]:
    fake_handler = FakeExternalEventHandler(bus=None)

    fake_external_events_map = {
        'fake.topic': fake_handler,
    }
    return fake_external_events_map
