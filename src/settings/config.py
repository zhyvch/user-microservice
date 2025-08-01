import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent

    DOCKER_RUN: bool = False

    USER_SERVICE_API_HOST: str = '127.0.0.1'
    USER_SERVICE_API_PORT: int
    USER_SERVICE_API_PREFIX: str = '/api/v1'
    USER_SERVICE_API_DOCS_URL: str = '/api/docs'
    USER_SERVICE_DEBUG: bool = True
    USER_SERVICE_MEDIA_PATH: str = 'user-service'
    USER_SERVICE_DEFAULT_USER_PHOTO: str = 'default_php.svg.png'

    JWT_ALGORITHM: str = 'RS256'

    RSA_PUBLIC_KEY_PATH: Path = BASE_PATH / 'keys/public.pem'

    REDIS_HOST: str
    REDIS_PORT: int

    CACHE_EXPIRATION_SECONDS: int = 60 * 60 * 24

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBITMQ_HOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str
    RABBITMQ_PORT: int

    NANOSERVICES_EXCH_NAME: str
    USER_SERVICE_QUEUE_NAME: str = 'user_service_queue'
    USER_SERVICE_CONSUMING_TOPICS: list[str] = ['user.#']

    LOG_LEVEL: int = logging.WARNING  # one of logging.getLevelNamesMapping().values()
    LOG_FORMAT: str = '[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)s - %(message)s'

    S3_SECRET_ACCESS_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str
    S3_PRESIGNED_EXPIRATION_SECONDS: int = 60 * 60

    AWS_S3_ACCESS_KEY_ID: str
    AWS_S3_REGION_NAME: str

    @property
    def REDIS_URL(self):
        return (
            f'redis://'
            f'{self.REDIS_HOST}:'
            f'{6379 if self.DOCKER_RUN else self.REDIS_PORT}/0'
        )

    @property
    def POSTGRES_URL(self):
        return (
            f'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:'
            f'{5432 if self.DOCKER_RUN else self.POSTGRES_PORT}/'
            f'{self.POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        case_sensitive=True,
    )


settings = Settings()  # type: ignore
