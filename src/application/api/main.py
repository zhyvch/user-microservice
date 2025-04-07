import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from punq import Container

from application.api.users.handlers import router
from application.external_events.consumers.base import BaseConsumer
from infrastructure.producers.base import BaseProducer
from settings.container import initialize_container
from settings.config import settings


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
    )
    app.include_router(router, prefix='/users')

    return app
