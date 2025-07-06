import string
import uuid

from random import randint, choices

import logging
import pytest
import pytest_asyncio

from application.external_events.consumers.rabbitmq import RabbitMQConsumer
from domain.entities.users import UserEntity
from domain.value_objects.users import EmailVO, PhoneNumberVO, NameVO
from infrastructure.producers.rabbitmq import RabbitMQProducer
from infrastructure.repositories.users.postgresql import SQLAlchemyUserRepository
from sqlalchemy.pool import NullPool
from infrastructure.storages.database import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from service.message_bus import MessageBus
from service.units_of_work.users.postgresql import SQLAlchemyUserUnitOfWork
from settings.container import get_commands_map, get_events_map, get_external_events_map
from .config import test_settings
from .fakes import FakeUserRepository, FakeUserUnitOfWork, FakeProducer, FakeConsumer


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
    uow = SQLAlchemyUserUnitOfWork(session_factory=postgres_session_factory)
    yield uow


@pytest.fixture
def message_bus(sqlalchemy_user_uow, rabbitmq_producer):
    bus = MessageBus(
        uow=sqlalchemy_user_uow,
        commands_map=get_commands_map(uow=sqlalchemy_user_uow),
        events_map=get_events_map(producer=rabbitmq_producer),
    )
    return bus


@pytest_asyncio.fixture
async def rabbitmq_producer():
    producer = RabbitMQProducer(
        host=test_settings.TESTS_RABBITMQ_HOST,
        port=test_settings.TESTS_RABBITMQ_PORT if not test_settings.DOCKER_RUN else '5432',
        login=test_settings.TESTS_RABBITMQ_USER,
        password=test_settings.TESTS_RABBITMQ_PASSWORD,
        virtual_host=test_settings.TESTS_RABBITMQ_VHOST,
        exchange_name=test_settings.TESTS_NANOSERVICES_EXCH_NAME,
    )
    await producer.start()
    yield producer
    await producer.stop()


@pytest_asyncio.fixture
async def rabbitmq_consumer(message_bus):
    consumer = RabbitMQConsumer(
        host=test_settings.TESTS_RABBITMQ_HOST,
        port=test_settings.TESTS_RABBITMQ_PORT if not test_settings.DOCKER_RUN else '5432',
        login=test_settings.TESTS_RABBITMQ_USER,
        password=test_settings.TESTS_RABBITMQ_PASSWORD,
        virtual_host=test_settings.TESTS_RABBITMQ_VHOST,
        queue_name=test_settings.TESTS_USER_SERVICE_QUEUE_NAME,
        exchange_name=test_settings.TESTS_NANOSERVICES_EXCH_NAME,
        consuming_topics=test_settings.TESTS_USER_SERVICE_CONSUMING_TOPICS,
        external_events_map=get_external_events_map(bus=message_bus),
    )
    await consumer.start()

    if consumer.queue:
        await consumer.queue.purge()

    yield consumer
    await consumer.stop()


@pytest.fixture
def valid_jwt():
    return 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MTRmNjBmNy0xMGE0LTQxNmMtODllZC1jODdhMTFjYWVlMWYiLCJzdWIiOiJkZjliN2FhNi1iNGU0LTRhMTktOGM4NC01MDRlMzAyZWVlOTgiLCJleHAiOjUzNDc0MjMwNzAsImlhdCI6MTc0NzQyMTI3MCwidHlwZSI6ImFjY2VzcyJ9.FwiVyt5cNZdrAcGlgOJi7i3LPZe8GQl266NgAT-Q-V963EGKK5OI1XCy9_dGgoDlrr6ooUBuebAXmZsJjVRWjj2ilWPOCoELEJmDCYy4e-AefdpCqNR0YGxCM2aRPHApwFAqGuPL-KX0HY2Qm-Tf6Y1QCF1qZ5k14Vy1G7Vrsrc'

@pytest.fixture
def expired_jwt():
    return 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3OGY0OGRkYi0zNDJjLTQ0MDgtYTViMS03NzM1NDkzMWEyYjkiLCJzdWIiOiJkZjliN2FhNi1iNGU0LTRhMTktOGM4NC01MDRlMzAyZWVlOTgiLCJleHAiOjE3NDc0MjMyMDQsImlhdCI6MTc0NzQyMTQwNCwidHlwZSI6ImFjY2VzcyJ9.TRuGI8htpvj-2UxZdW_AJrj-bu3oRzu57RLVZrq_Rc2rtL6XRCOag4LQQgC4JzWwHYGYRyatazK_btmvR--pVWA8Gd2b1ZMKZ1BmWmsD4Tpe03TuBT86nIGKc3NUIV2Rmws4rMxGEuKGJwvExH_CYRe_ej53TOLgcXabVtxDuek'

@pytest.fixture
def wrong_type_jwt():
    return 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkMTFkYTQzNS1iODk3LTQ4MTctOTJiOC1jNmNjZjY4NjhiMzMiLCJzdWIiOiJkZjliN2FhNi1iNGU0LTRhMTktOGM4NC01MDRlMzAyZWVlOTgiLCJleHAiOjUzNDgwMjYwNzAsImlhdCI6MTc0NzQyMTI3MCwidHlwZSI6InJlZnJlc2gifQ.XTAH5ANAP5ow3wZdov0sPM9dRM9hVppNc-9OR4jgQfhuEvbBJN_ch6WeoLaCOr55AhnzQLRLXW71XqazFCnc5IYNah9iRQuAlU_FdbuvUalKLwWCpUDcE5qVWJgRaJKgAm7j6ven7C4AGItZNukVRhlRM_LYRuLh77J02fG9A-M'


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
    return FakeUserUnitOfWork()


@pytest.fixture
def fake_message_bus(fake_user_uow, fake_producer):
    bus = MessageBus(
        uow=fake_user_uow,
        commands_map=get_commands_map(uow=fake_user_uow),
        events_map=get_events_map(producer=fake_producer),
    )
    return bus


@pytest.fixture
def fake_producer():
    return FakeProducer()


@pytest.fixture()
def fake_consumer(fake_message_bus):
    consumer = FakeConsumer(
        topics_to_consume=test_settings.TESTS_USER_SERVICE_CONSUMING_TOPICS,
        external_events_map=get_external_events_map(bus=fake_message_bus),
    )
    return consumer
