import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent

    USER_SERVICE_API_PORT: int
    USER_SERVICE_DEBUG: bool
    USER_SERVICE_MEDIA_PATH: str = 'user-service'

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
    USER_SERVICE_CONSUMING_RKS: list[str] = ['user.credentials.created', 'user.credentials.updated']

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
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0'

    @property
    def POSTGRES_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{5432}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        case_sensitive=True,
    )

settings = Settings()  # type: ignore
