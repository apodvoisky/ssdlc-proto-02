import sys
from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from models.data.customer import Customer
from models.schemas.schema import CustomerReqBase
from services.customer import CustomerService
from infra.depends import SSDLCContainer
from infra.exceptions import EntityNotFoundError


router = APIRouter()


@router.post(
    "/customer",
    status_code=status.HTTP_201_CREATED,
    tags=['Customer'],
)
@inject
async def add(req: CustomerReqBase, customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    return await customer_service.create(req)


@router.patch(
    "/customer",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            'response': status.HTTP_404_NOT_FOUND,
            'description': 'Specified customer does not exists'
        }
    },
    tags=['Customer'],
)
@inject
async def update(
        customer_id: int,
        req: CustomerReqBase,
        customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    try:
        return await customer_service.update(customer_id=customer_id, customer=req)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/customer/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            'response': status.HTTP_404_NOT_FOUND,
            'description': 'Specified customer does not exists'
        }
    },
    tags=['Customer'],
)
@inject
async def delete(customer_id: int, customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    try:
        return await customer_service.delete(customer_id=customer_id)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/customer",
    status_code=status.HTTP_200_OK,
    tags=['Customer'],
)
@inject
async def get_customer(customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    return await customer_service.get_all()


@router.get(
    "/customer/{customer_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            'response': status.HTTP_404_NOT_FOUND,
            'description': 'Specified customer does not exists'
        }
    },
    tags=['Customer'],
)
@inject
async def get(customer_id: int, customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    try:
        customer: Customer = await customer_service.get(customer_id)
        return customer
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
