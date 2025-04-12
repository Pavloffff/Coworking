from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError


class TokenProcessor:
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
