from abc import ABC,abstractmethod
from dataclasses import dataclass


@dataclass
class BaseS3Client(ABC):
    access_key: str
    secret_key: str
    bucket_name: str
    endpoint_url: str

    @abstractmethod
    async def upload_file(self, ) -> None:
        ...



