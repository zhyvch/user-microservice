from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent

    DOCKER_RUN: bool = False

    TESTS_POSTGRES_HOST: str
    TESTS_POSTGRES_PORT: int
    TESTS_POSTGRES_USER: str
    TESTS_POSTGRES_PASSWORD: str
    TESTS_POSTGRES_DB: str

    TESTS_RABBITMQ_HOST: str
    TESTS_RABBITMQ_USER: str
    TESTS_RABBITMQ_PASSWORD: str
    TESTS_RABBITMQ_VHOST: str
    TESTS_RABBITMQ_PORT: int

    TESTS_USER_SERVICE_QUEUE_NAME: str = 'tests_user_service_queue'
    TESTS_NANOSERVICES_EXCH_NAME: str
    TESTS_USER_SERVICE_CONSUMING_TOPICS: list[str] = ['fake.user.topic', 'user.credentials.created', 'user.credentials.updated']

    @property
    def TESTS_POSTGRES_URL(self):
        return (
            f'postgresql+asyncpg://'
            f'{self.TESTS_POSTGRES_USER}:'
            f'{self.TESTS_POSTGRES_PASSWORD}@'
            f'{self.TESTS_POSTGRES_HOST}:'
            f'{5432 if self.DOCKER_RUN else self.TESTS_POSTGRES_PORT}/'
            f'{self.TESTS_POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env.tests',
        case_sensitive=True,
    )


test_settings = TestSettings() # type: ignore
