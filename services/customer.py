from repository.customer import CustomerRepository
from models.requests.customer import CustomerReq


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

    async def create(self, customer: CustomerReq):
        return self.customer_repository.create_user(customer)
