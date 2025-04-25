import logging
from dataclasses import dataclass
from uuid import UUID

from redis.asyncio import Redis

from domain.entities.users import UserEntity
from infrastructure.cache.base import BaseUserRepositoryCacher
from infrastructure.converters.users import convert_user_json_to_entity, convert_user_entity_to_json
from infrastructure.storages.cache import get_redis_client
from settings.config import settings

logger = logging.getLogger(__name__)


@dataclass
class RedisUserRepositoryCacher(BaseUserRepositoryCacher):
    redis: Redis = get_redis_client()

    async def get_from_cache(self, user_id: UUID) -> UserEntity | None:
        logger.debug('Retrieving user \'%s\' from Redis cache', user_id)
        try:
            user = await self.redis.get(f'user:{user_id}')
            if user:
                logger.debug('User \'%s\' found in Redis cache', user_id)
                return convert_user_json_to_entity(user)
            logger.debug('User \'%s\' not found in Redis cache', user_id)
            return None
        except Exception as e:
            logger.exception('Error retrieving user \'%s\' from Redis cache: %s', user_id, str(e))
            return None

    async def add_to_cache(self, user: UserEntity) -> None:
        logger.debug('Adding user \'%s\' to Redis cache', user.id)
        try:
            await self.redis.set(
                name=f'user:{user.id}',
                value=convert_user_entity_to_json(user),
                ex=settings.CACHE_EXPIRATION_SECONDS,
            )
            logger.debug(
                'User \'%s\' added to Redis cache with expiration %d seconds',
                user.id,
                settings.CACHE_EXPIRATION_SECONDS
            )
        except Exception as e:
            logger.exception('Failed to add user \'%s\' to Redis cache: %s', user.id, str(e))
            raise

    async def remove_from_cache(self, user_id: UUID) -> None:
        logger.debug('Removing user \'%s\'from Redis cache', user_id)
        try:
            result = await self.redis.delete(f'user:{user_id}')
            if result:
                logger.debug('User \'%s\' removed from Redis cache', user_id)
            else:
                logger.debug('User \'%s\' was not in Redis cache', user_id)
        except Exception as e:
            logger.exception('Error removing user \'%s\' from Redis cache: %s', user_id, str(e))
            raise

cache_repository = RedisUserRepositoryCacher()
