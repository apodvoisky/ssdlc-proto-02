import sys
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from app.infra.depends import SSDLCContainer

import app.settings as settings
from app.models.schemas.schema import Token
from app.services.security import create_access_token
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/token",
    tags=["Security"],
    response_model=Token
)
@inject
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(Provide[SSDLCContainer.user_service])
):
    user = await user_service.get_by_email(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Имя пользователя задано неверно.",
        )

    authenticated = user.verify_password(form_data.password)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль указан неверно.",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
