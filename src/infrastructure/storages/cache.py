from redis.asyncio import Redis, ConnectionPool

from settings.config import settings


redis_pool = ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=10,
)

def get_redis_client() -> Redis:
    return Redis(connection_pool=redis_pool)
