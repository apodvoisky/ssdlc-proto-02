from datetime import datetime
from datetime import timedelta
import time
from typing import Optional

from jose import jwt
from jose import JWTError
from fastapi import HTTPException
from fastapi import status
from app.services.user import UserService

#TODO setting в контейнер?
import app.settings as settings

import app.infra.depends


class SecurityService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        jwt_secret_key = app.infra.depends.SSDLCContainer.config()['auth']['jwt_secret_key']
        jwt_algorithm = app.infra.depends.SSDLCContainer.config()['auth']['jwt_algorithm']
        access_token_expire_in_min = app.infra.depends.SSDLCContainer.config()['auth']['access_token_expire_in_min']

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=access_token_expire_in_min
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, jwt_secret_key, algorithm=jwt_algorithm
        )
        return encoded_jwt

    @staticmethod
    async def get_user_from_token(
            token: str,
            user_service: UserService):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка проверки учетных данных.",
        )
        jwt_secret_key = app.infra.depends.SSDLCContainer.config()['auth']['jwt_secret_key']
        jwt_algorithm = app.infra.depends.SSDLCContainer.config()['auth']['jwt_algorithm']

        try:
            payload = jwt.decode(
                token, jwt_secret_key, algorithms=[jwt_algorithm]
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


