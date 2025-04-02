import hashlib
import os
import binascii


class Hasher:
    @staticmethod
    def hash(password: str) -> tuple[str, str]:
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=salt,
            iterations=100000
        )
        return (
            binascii.hexlify(hashed_password).decode(), 
            binascii.hexlify(salt).decode()
        )
