from infrastructure.storages.s3.clients.base import BaseS3Client


class AWSS3Client(BaseS3Client):
    async def upload_file(self, ) -> None:
        ...
