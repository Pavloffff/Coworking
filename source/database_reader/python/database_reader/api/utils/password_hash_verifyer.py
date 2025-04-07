import binascii
import hashlib


class PasswordHashVerifyer:
    @staticmethod
    def verify(password: str, password_hash: str, salt_str: str, iterations: int):    
        salt = binascii.unhexlify(salt_str)
        new_hash = hashlib.pbkdf2_hmac(
            hash_name='sha256', password=password.encode(), salt=salt, iterations=iterations
        )
        return password_hash == binascii.hexlify(new_hash).decode()
