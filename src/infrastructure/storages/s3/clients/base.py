from abc import ABC,abstractmethod

from settings.config import settings


class BaseS3Client(ABC):
    secret_access_key: str = settings.S3_SECRET_ACCESS_KEY
    endpoint_url: str = settings.S3_ENDPOINT_URL
    bucket_name: str = settings.S3_BUCKET_NAME

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
