from repository.customer import CustomerRepository
from models.requests.customerreq import CustomerReqBase


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def get_all(self):
        customers = await self.customer_repository.get_all()
        return customers

    async def get(self, customer_id: int):
        customer = await self.customer_repository.get(customer_id)
        if not customer:
            raise ValueError("Заказчик не найден")
        return customer

    async def create(self, customer: CustomerReqBase):
        return await self.customer_repository.insert(customer)

    async def delete(self, customer_id: int):
        return await self.customer_repository.delete(customer_id)

    async def update(self, customer_id: int, customer: CustomerReqBase):
        return await self.customer_repository.update(customer_id, customer)