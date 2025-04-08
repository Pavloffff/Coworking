from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError


class TokenProcessor:
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
    
    @staticmethod
    def verify(token: str, secret_key: str):
        try:
            payload = jwt.decode(
                    token,
                    secret_key,
                    algorithms=["HS256"],
                    options={"require_sub": True}
                )
            email = payload.get("sub")
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    @staticmethod
    def decode_without_validation(token: str) -> dict:
        return jwt.get_unverified_claims(token)
