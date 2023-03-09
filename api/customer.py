from fastapi import APIRouter
from db_config.sqlalchemy_async_connect import AsynSessionFactory
from repository.customer import CustomerRepository
from models.requests.customer import CustomerReq
from models.data.customer import Customer

router = APIRouter()


@router.post("/customer")
async def add(req: CustomerReq):
    async with AsynSessionFactory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            customer = Customer(id=req.id, first_name=req.first_name, second_name=req.second_name,
                                sur_name=req.sur_name, cell_phone=req.cell_phone, email=req.email)

            return await repo.insert(customer)


@router.patch("/customer")
async def update(id: int, req: CustomerReq):
    async with AsynSessionFactory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            customer_dict = req.dict(exclude_unset=True)
            return await repo.update(id, customer_dict)


@router.delete("/customer/{id}")
async def delete(id: int):
    async with AsynSessionFactory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            return await repo.delete(id)


@router.get("/customer")
async def get():
    async with AsynSessionFactory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            return await repo.get_all()


@router.get("/customer/{id}")
async def get(id: int):
    async with AsynSessionFactory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            return await repo.get(id)
