import sys
from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from app.models.data.customer import Customer
from app.models.schemas.schema import CustomerCreate, Products, CustomerUpdate
from app.services.customer import CustomerService
from app.services.product import ProductService
from app.infra.depends import SSDLCContainer
from app.infra.exceptions import EntityNotFoundError


router = APIRouter()


@router.post(
    "/customers",
    status_code=status.HTTP_201_CREATED,
    tags=["Customer"],
    summary="Добавить нового потребителя",
)
@inject
async def add(
        req: CustomerCreate,
        customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    return await customer_service.create(req)


@router.patch(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified customer does not exists"
        }
    },
    tags=["Customer"],
    summary="Обновить данные потребителя по его идентификатору",
)
@inject
async def update(
        customer_id: int,
        req: CustomerUpdate,
        customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    try:
        return await customer_service.update(customer_id=customer_id, customer=req)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/customers/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified customer does not exists"
        }
    },
    tags=["Customer"],
    summary="Удалить данные по потребителю по его идентификатору.",
)
@inject
async def delete(customer_id: int, customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    try:
        return await customer_service.delete(customer_id=customer_id)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/customers",
    status_code=status.HTTP_200_OK,
    tags=["Customer"],
    summary="Получить список всех потребителей.",
)
@inject
async def get_customer(customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    return await customer_service.get_all()


@router.get(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified customer does not exists"
        }
    },
    tags=["Customer"],
    summary="Получить потребителя по его идентификатору.",
)
@inject
async def get(customer_id: int, customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    try:
        customer: Customer = await customer_service.get(customer_id)
        return customer
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/customers/{customer_id}/products",
    status_code=status.HTTP_200_OK,
    response_model=Products,
    responses={
        404: {
            "response": status.HTTP_404_NOT_FOUND,
            "description": "Specified customer does not exists"
        }
    },
    tags=["Customer"],
    summary="Получить данные по продуктам потребителя по его идентификатору.",
)
@inject
async def get_products(customer_id: int, products_service: ProductService = Depends(Provide[SSDLCContainer.product_service])):
    try:
        products: Customer = await products_service.get_customer_products(customer_id)
        return products
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/customers/test/")
@inject
async def test(sess=Depends(Provide[SSDLCContainer.async_session])):
    from app.models.data.customer import Customer
    from app.models.data.product import Product

    async with sess.begin():
        customer1 = Customer(
            first_name="Customer1",
            second_name="Customer1",
            sur_name="Customer1",
            cell_phone="Customer1",
            email="Customer1",
            products=[
                Product(
                    title="Product1",
                    code="Product1",
                ),
                Product(
                    title="Product2",
                    code="Product2",
                ),
            ]
        )
        sess.add_all([customer1])
        await sess.commit()


container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])

