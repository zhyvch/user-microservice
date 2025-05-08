from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    BASE_PATH: Path = Path(__file__).resolve().parent.parent

    TESTS_POSTGRES_HOST: str
    TESTS_POSTGRES_PORT: int
    TESTS_POSTGRES_USER: str
    TESTS_POSTGRES_PASSWORD: str
    TESTS_POSTGRES_DB: str

    @property
    def TESTS_POSTGRES_URL(self):
        return f'postgresql+asyncpg://{self.TESTS_POSTGRES_USER}:{self.TESTS_POSTGRES_PASSWORD}@{self.TESTS_POSTGRES_HOST}:{5432}/{self.TESTS_POSTGRES_DB}'

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env.tests',
        case_sensitive=True,
    )


test_settings = TestSettings() # type: ignore
