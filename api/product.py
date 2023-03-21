import sys
from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from models.data.product import Product
from models.schemas.schema import ProductBase, ProductCreate, ProductUpdate
from services.product import ProductService
from infra.depends import SSDLCContainer
from infra.exceptions import EntityNotFoundError
from repository.customer import CustomerNotFoundError
from repository.product import ProductNotFoundError


router = APIRouter()


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    tags=["Product"],
    summary="Добавить новый продукт.",
)
@inject
async def add(req: ProductCreate, product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    return await product_service.create(req)


@router.patch(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified product does not exists"
        }
    },
    tags=["Product"],
    summary="Обновить данные по продукту по его идентификатору.",
)
@inject
async def update(
        product_id: int,
        req: ProductUpdate,
        product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        return await product_service.update(product_id=product_id, product=req)
    except CustomerNotFoundError as cnfe:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(cnfe))
    except ProductNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified product does not exists"
        }
    },
    tags=["Product"],
    summary="Удалить продукт по его идентификатору.",
)
@inject
async def delete(product_id: int, product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        return await product_service.delete(product_id=product_id)
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
async def get(product_id: int, product_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        product: Product = await product_service.get(product_id)
        return product
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
