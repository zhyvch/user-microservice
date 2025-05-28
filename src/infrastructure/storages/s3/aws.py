import logging
from dataclasses import dataclass

from aiobotocore.session import AioSession, get_session

from infrastructure.storages.s3.base import BaseS3Client
from settings.config import settings


logger = logging.getLogger(__name__)


@dataclass
class AWSS3Client(BaseS3Client):
    aws_access_key_id: str
    aws_region_name: str
    session: AioSession

    async def generate_presigned_upload_post(
            self,
            key: str,
            content_type: str,
            expires_in: int = settings.S3_PRESIGNED_EXPIRATION_SECONDS,
    ) -> dict:
        logger.debug('Generating presigned upload POST for key: %s', key)
        async with self.session.create_client(
                's3',
                region_name=self.aws_region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.secret_access_key,
                endpoint_url=self.endpoint_url,
        ) as client:
            try:
                response = await client.generate_presigned_post(
                    Bucket=self.bucket_name,
                    Key=key,
                    Fields={
                        'Content-Type': content_type,
                    },
                    Conditions=[
                        {'Content-Type': content_type}
                    ],
                    ExpiresIn=expires_in
                )
                logger.debug('Generated presigned upload POST for key: %s', key)
                return response
            except Exception as e:
                logger.exception('Failed to generate presigned upload POST for key %s: %s', key, str(e))
                raise

    async def generate_presigned_download_url(
            self,
            key: str,
            content_type: str,
            expires_in: int = settings.S3_PRESIGNED_EXPIRATION_SECONDS,
    ) -> str:
        logger.debug('Generating presigned download URL for key: %s', key)
        async with self.session.create_client(
                's3',
                region_name=self.aws_region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.secret_access_key,
                endpoint_url=self.endpoint_url,
        ) as client:
            try:
                url = await client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': self.bucket_name,
                        'Key': key,
                        'ResponseContentType': content_type,
                    },
                    ExpiresIn=expires_in
                )
                logger.debug('Generated presigned download URL for key: %s', key)
                return url
            except Exception as e:
                logger.exception('Failed to generate presigned download URL for key %s: %s', key, str(e))
                raise
