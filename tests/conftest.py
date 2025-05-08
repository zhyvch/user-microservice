import string
import uuid

from random import randint, choices

import logging
import pytest
import pytest_asyncio

from domain.entities.users import UserEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO
from infrastructure.repositories.users.postgresql import SQLAlchemyUserRepository
from sqlalchemy.pool import NullPool
from infrastructure.storages.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from service.message_bus import MessageBus
from service.units_of_work.users.postgresql import SQLAlchemyUserUnitOfWork
from settings.config import settings
from settings.container import get_commands_map, get_events_map, get_external_events_map
from .config import test_settings
from .fakes import FakeUserRepository, FakeUnitOfWork, FakeProducer, FakeConsumer

logger = logging.getLogger(__name__)


SKIP_DIRS = {'e2e', 'integration'}

def pytest_addoption(parser):
    parser.addoption(
        '--run-all',
        action='store_true',
        default=False,
        help='run all tests'
    )

def pytest_ignore_collect(collection_path, config):
    if not config.getoption('--run-all') and collection_path.name in SKIP_DIRS:
        return True
    return None



@pytest_asyncio.fixture(scope='session')
async def postgres_db():
    engine = create_async_engine(
        test_settings.TESTS_POSTGRES_URL,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
def postgres_session_factory(postgres_db):
    return async_sessionmaker(
        bind=postgres_db,
        expire_on_commit=False
    )


@pytest_asyncio.fixture
async def sqlalchemy_user_repository(postgres_session_factory):
    session = postgres_session_factory()
    repo = SQLAlchemyUserRepository(session=session)
    yield repo
    await session.close()


@pytest.fixture
def sqlalchemy_user_uow(postgres_session_factory):
    uow = SQLAlchemyUserUnitOfWork()
    uow.session_factory = postgres_session_factory
    yield uow


@pytest.fixture
def random_user_entity():
    oid = uuid.uuid4()
    return UserEntity(
        id=oid,
        email=EmailVO(f'user_{oid}@example.com'),
        phone_number=PhoneNumberVO(f'+{randint(1000000000, 9999999999)}'),
        first_name=NameVO(''.join(choices(string.ascii_letters, k=10))),
        last_name=NameVO(''.join(choices(string.ascii_letters, k=10))),
        middle_name=NameVO(''.join(choices(string.ascii_letters, k=10))),
    )


@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()


@pytest.fixture
def fake_user_uow():
    return FakeUnitOfWork()


@pytest.fixture
def fake_message_bus(fake_user_uow, fake_producer):
    bus = MessageBus(
        uow=fake_user_uow,
        commands_map=get_commands_map(uow=fake_user_uow),
        events_map=get_events_map(producer=fake_producer)
    )
    return bus


@pytest.fixture
def fake_producer():
    return FakeProducer()


@pytest.fixture()
def fake_consumer(fake_message_bus):
    consumer = FakeConsumer(
        topics_to_consume=settings.USER_SERVICE_CONSUMING_TOPICS,
        external_events_map=get_external_events_map(bus=fake_message_bus)
    )
    return consumer
