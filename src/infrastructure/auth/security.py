from functools import lru_cache

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from settings.config import settings


@lru_cache(1)
def get_public_key() -> RSAPublicKey:
    with open(settings.RSA_PUBLIC_KEY_PATH, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
        return public_key
