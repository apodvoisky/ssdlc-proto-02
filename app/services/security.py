from datetime import datetime
from datetime import timedelta
import time
from typing import Optional

from jose import jwt
from jose import JWTError

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

#from app.infra.depends import SSDLCContainer
from app.services.user import UserService
from dependency_injector.wiring import inject, Provide

#TODO setting в контейнер?
import app.settings as settings


class SecurityService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    async def get_user_from_token(
            token: str,
            user_service: UserService):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await user_service.get_by_email(email=email)
        if user is None:
            raise credentials_exception
        return user


