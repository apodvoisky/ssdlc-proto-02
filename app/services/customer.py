from app.repository.customer import CustomerRepository
from app.models.schemas.schema import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def get_all(self):
        customers = await self.customer_repository.get_all()
        return customers

    async def get(self, customer_id: int):
        customer = await self.customer_repository.get(customer_id)
        return customer

    async def create(self, customer: CustomerCreate):
        return await self.customer_repository.insert(customer)

    async def delete(self, customer_id: int):
        return await self.customer_repository.delete(customer_id)

    async def update(self, customer_id: int, customer: CustomerUpdate):
        return await self.customer_repository.update(customer_id, customer)
