from abc import ABC,abstractmethod
from dataclasses import dataclass

from settings.config import settings


# TODO: Make a repo from it?


@dataclass
class BaseS3Client(ABC):
    secret_access_key: str
    endpoint_url: str
    bucket_name: str

    @abstractmethod
    async def generate_presigned_upload_post(
            self,
            key: str,
            content_type: str,
            expires_in: int = settings.S3_PRESIGNED_EXPIRATION_SECONDS,
    ) -> dict:
        ...

    @abstractmethod
    async def generate_presigned_download_url(
            self,
            key: str,
            content_type: str,
            expires_in: int = settings.S3_PRESIGNED_EXPIRATION_SECONDS,
    ) -> str:
        ...
