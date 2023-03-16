import sys
from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from typing import List
from models.data.customer import Customer
from models.requests.customer import CustomerReq
from repository.customer import CustomerRepository
from services.customer import CustomerService
from infra.depends import get_customer_service, get_dep_str, SSDLCContainer, TestService
from db_config.sqlalchemy_async_connect import SessionFactory


router = APIRouter()


@router.post("/customer", status_code=201)
async def add(req: CustomerReq):
    async with async_session_factory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            customer = Customer(
                            first_name=req.first_name,
                            second_name=req.second_name,
                            sur_name=req.sur_name,
                            cell_phone=req.cell_phone,
                            email=req.email)

            result = await repo.insert(customer)
            if not result["result"]:
                raise HTTPException(status_code=400, detail=result["message"])

            return True


@router.patch("/customer")
async def update(id: int, req: CustomerReq):
    raise NotImplementedError()

    async with async_session_factory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            customer_dict = req.dict(exclude_unset=True)
            return await repo.update(id, customer_dict)


@router.delete("/customer/{id}")
async def delete(id: int):
    raise NotImplementedError()

    async with async_session_factory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            return await repo.delete(id)


@router.get("/customer") #, response_model=List[CustomerReq])
@inject
async def get_customer(customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    return await customer_service.get_all()


@router.get("/customer2")
@inject
async def get_customer2(customer_repo: CustomerRepository = Depends(Provide[SSDLCContainer.customer_repository])):
    raise NotImplementedError()


@router.get("/customer3")
@inject
async def get_customer3(sess = Depends(Provide[SSDLCContainer.async_session])):
    repo = CustomerRepository(sess)
    all_cust = await repo.get_all()
    return all_cust

@router.get("/customer/{id}") #, response_model=List[CustomerReq])
async def get(id: int, customer_service: CustomerService = Depends(Provide[SSDLCContainer.customer_service])):
    return await customer_service.get(id)


def get_str() -> str:
    return "hello!!!"


def get_str2():
    return "message!!!"


@router.get("/")
@inject
async def test(val: str = Depends(get_str), service: TestService = Depends(Provide[SSDLCContainer.test_service])):
    msg = await service.process()
    return {msg: val}


container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
