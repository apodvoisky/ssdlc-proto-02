import sys
from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from app.models.data.user import User
from app.models.schemas.schema import UserCreate, Products, UserUpdate
from app.services.user import UserService
from app.services.product import ProductService
from app.infra.depends import SSDLCContainer
from app.infra.exceptions import EntityNotFoundError


router = APIRouter()


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
    summary="Добавить нового пользователя",
)
@inject
async def add(
        req: UserCreate,
        user_service: UserService = Depends(Provide[SSDLCContainer.user_service])):
    return await user_service.create(req)


@router.patch(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified user does not exists"
        }
    },
    tags=["User"],
    summary="Обновить данные пользователя по его идентификатору",
)
@inject
async def update(
        user_id: int,
        req: UserUpdate,
        user_service: UserService = Depends(Provide[SSDLCContainer.user_service])):
    try:
        return await user_service.update(user_id=user_id, user=req)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified user does not exists"
        }
    },
    tags=["User"],
    summary="Удалить данные пользователя по его идентификатору.",
)
@inject
async def delete(
        user_id: int,
        user_service: UserService = Depends(Provide[SSDLCContainer.user_service])):
    try:
        return await user_service.delete(user_id=user_id)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Получить список всех пользователей.",
)
@inject
async def get_user(user_service: UserService = Depends(Provide[SSDLCContainer.user_service])):
    return await user_service.get_all()


@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified user does not exists"
        }
    },
    tags=["User"],
    summary="Получить пользователя по его идентификатору.",
)
@inject
async def get(user_id: int, user_service: UserService = Depends(Provide[SSDLCContainer.user_service])):
    try:
        user: User = await user_service.get(user_id)
        return user
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))



container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
