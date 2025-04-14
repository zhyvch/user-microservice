from dataclasses import dataclass
from uuid import UUID

from redis.asyncio import Redis

from domain.entities.users import UserEntity
from infrastructure.cache.base import BaseUserRepositoryCacher
from infrastructure.converters.users import convert_user_json_to_entity, convert_user_entity_to_json
from infrastructure.storages.cache import get_redis_client
from settings.config import settings


@dataclass
class RedisUserRepositoryCacher(BaseUserRepositoryCacher):
    redis: Redis = get_redis_client()

    async def get_from_cache(self, user_id: UUID) -> UserEntity | None:
        user = await self.redis.get(f'user:{user_id}')
        if user:
            return convert_user_json_to_entity(user)

    async def add_to_cache(self, user: UserEntity) -> None:
        await self.redis.set(
            name=f'user:{user.id}',
            value=convert_user_entity_to_json(user),
            ex=settings.CACHE_EXPIRATION_SECONDS,
        )

    async def remove_from_cache(self, user_id: UUID) -> None:
        await self.redis.delete(f'user:{user_id}')

cache_repository = RedisUserRepositoryCacher()
