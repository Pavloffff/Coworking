from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


class TokenGenerator:
    @staticmethod
    def generate(
        subject: Union[str, Any], 
        expires_delta: int = None, 
        expire: int = 20, 
        secret_key: str = '',
    ) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=expire)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, secret_key, "HS256")
        return encoded_jwt
    