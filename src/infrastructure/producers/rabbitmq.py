import logging
import aio_pika
import orjson
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractExchange

from domain.events.base import BaseEvent
from infrastructure.producers.base import BaseProducer
from settings.config import settings

logger = logging.getLogger(__name__)


class RabbitMQProducer(BaseProducer):
    connection: AbstractRobustConnection
    channel: AbstractRobustChannel
    exchange: AbstractExchange

    async def start(self):
        logger.info(
            'Establishing connection to RabbitMQ at %s:%d',
            settings.RABBITMQ_HOST,
            settings.RABBITMQ_PORT,
        )
        try:
            self.connection = await aio_pika.connect_robust(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                login=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASSWORD,
                virtual_host=settings.RABBITMQ_VHOST,
            )
            logger.debug('RabbitMQ connection established')

            self.channel = await self.connection.channel()
            logger.debug('RabbitMQ channel created')

            self.exchange = await self.channel.get_exchange(name=settings.NANOSERVICES_EXCH_NAME)
            logger.info('Connected to RabbitMQ exchange \'%s\'', settings.NANOSERVICES_EXCH_NAME)
        except Exception as e:
            logger.critical('Failed to connect to RabbitMQ: %s', str(e), exc_info=True)
            raise

    async def stop(self):
        logger.info('Closing RabbitMQ connections')
        try:
            if hasattr(self, 'channel') and self.channel:
                logger.debug('Closing RabbitMQ channel')
                await self.channel.close()

            if hasattr(self, 'connection') and self.connection:
                logger.debug('Closing RabbitMQ connection')
                await self.connection.close()

            logger.info('RabbitMQ connections closed successfully')
        except Exception as e:
            logger.critical('Error closing RabbitMQ connections: %s', str(e), exc_info=True)
            raise

    async def publish(self, event: BaseEvent, topic: str):
        logger.debug('Publishing %s event to topic \'%s\'', event.__class__.__name__, topic)

        if not hasattr(self, 'connection') or not self.connection or not hasattr(self, 'exchange') or not self.exchange:
            logger.debug('RabbitMQ connection not established, starting connection')
            await self.start()

        try:
            await self.exchange.publish(
                aio_pika.Message(
                    body=orjson.dumps(event.__dict__),
                    content_type='application/json',
                ),
                routing_key=topic,
            )
            logger.info(
                'Published %s event to topic \'%s\'',
                event.__class__.__name__,
                topic,
            )
        except Exception as e:
            logger.exception(
                'Failed to publish %s event to topic \'%s\': %s',
                event.__class__.__name__,
                topic,
                str(e)
            )
            raise
