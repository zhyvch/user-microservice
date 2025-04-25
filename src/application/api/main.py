import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from punq import Container

from application.api.exception_handlers import exception_registry
from application.api.v1.users.handlers import router
from application.external_events.consumers.base import BaseConsumer
from infrastructure.producers.base import BaseProducer
from settings.container import initialize_container
from settings.config import settings

API_V1_PREFIX = '/api/v1'

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = initialize_container()
    consumer: BaseConsumer = container.resolve(BaseConsumer)
    producer: BaseProducer = container.resolve(BaseProducer)

    await consumer.start()
    consume_task = asyncio.create_task(consumer.consume())

    await producer.start()

    yield

    await producer.stop()

    consume_task.cancel()
    await consumer.stop()


def create_app():
    app = FastAPI(
        title='User Service',
        description='Simple user service',
        docs_url='/api/docs',
        debug=settings.USER_SERVICE_DEBUG,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )
    app.include_router(router, prefix=API_V1_PREFIX)
    exception_registry(app)

    return app
