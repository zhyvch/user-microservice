from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).parent.parent.parent

    USER_SERVICE_API_PORT: int
    USER_SERVICE_DEBUG: bool

    JWT_ALGORITHM: str = 'RS256'
    RSA_PUBLIC_KEY_PATH: Path = BASE_PATH / 'keys/public.pem'

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: int
    RABBITMQ_VHOST: str
    RABBITMQ_PORT: int

    @property
    def POSTGRES_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        case_sensitive=True
    )


settings = Settings()
