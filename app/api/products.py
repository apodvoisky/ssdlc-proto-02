import sys
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from app.models.data.product import Product
from app.models.schemas.schema import ProductCreate, ProductUpdate, Product
from app.services.product import ProductService
from app.infra.depends import SSDLCContainer
from app.infra.exceptions import (
    EntityNotFoundError,
    ProductTitleAlreadyExists,
    ProductCodeAlreadyExists,
)
from app.repository.customer import CustomerNotFoundError
from app.repository.product import ProductNotFoundError


router = APIRouter()


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    tags=["Product"],
    summary="Добавить новый продукт.",
    responses={
        400: {
            "response": status.HTTP_400_BAD_REQUEST,
            "description": "Ошибка аргументов, невозможно создать продукт."
        },
    },
    response_model=Product
)
@inject
async def add(req: ProductCreate, product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        result = await product_service.create(req)
        return Product.parse_obj(result.__dict__)

    except ProductTitleAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'Продукт с наименованием {req.title} уже зарегистрирован.')
    except ProductCodeAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'Продукт с кодом {req.code} уже зарегистрирован.')


@router.patch(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "response": status.HTTP_400_BAD_REQUEST,
            "description": "Ошибка аргументов, невозможно обновить продукт."
        },
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Указанный продукт не зарегистрирован."
        }
    },
    tags=["Product"],
    summary="Обновить данные по продукту по его идентификатору.",
    response_model=Product,
)
@inject
async def update(
        product_id: UUID,
        req: ProductUpdate,
        product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        result = await product_service.update(product_id=product_id, product=req)
        return Product.parse_obj(result.__dict__)

    except CustomerNotFoundError as cnfe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(cnfe))
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductTitleAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'Продукт с наименованием {req.title} уже зарегистрирован.')
    except ProductCodeAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'Продукт с кодом {req.code} уже зарегистрирован.')


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Указанный продукт не зарегистрирован."
        }
    },
    tags=["Product"],
    summary="Удалить продукт по его идентификатору.",
)
@inject
async def delete(product_id: UUID, product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        await product_service.delete(product_id=product_id)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/products",
    status_code=status.HTTP_200_OK,
    tags=["Product"],
    summary="Получить данные по всем продуктам."
)
@inject
async def get_product(product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    return await product_service.get_all()


@router.get(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified product does not exists"
        }
    },
    tags=["Product"],
    summary="Получить данные продукта по его идентификатору",
)
@inject
async def get(product_id: UUID, product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        product: Product = await product_service.get(product_id)
        return product
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
