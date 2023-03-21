from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models.data.customer import Customer
from infra.exceptions import EntityNotFoundError
from models.schemas.schema import CustomerBase, CustomerCreate, CustomerUpdate


class CustomerNotFoundError(EntityNotFoundError):
    entity_name: str = "Customer"


class CustomerRepository:
    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, data: CustomerCreate):
        async with self.sess.begin():
            customer = Customer(
                first_name=data.first_name,
                sur_name=data.sur_name,
                second_name=data.second_name,
                cell_phone=data.cell_phone,
                email=data.email)

            self.sess.add(customer)
            await self.sess.commit()

            return customer

    async def update(self, customer_id: int, customer: CustomerUpdate) -> bool:
        async with self.sess.begin():
            customer_exists = await self.check(customer_id)
            if not customer_exists:
                raise CustomerNotFoundError(customer_id)

            q = update(Customer).where(Customer.id == customer_id)

            if customer.first_name:
                q = q.values(first_name=customer.first_name)
            if customer.sur_name:
                q = q.values(sur_name=customer.sur_name)
            if customer.second_name:
                q = q.values(second_name=customer.second_name)
            if customer.cell_phone:
                q = q.values(cell_phone=customer.cell_phone)
            if customer.email:
                q = q.values(email=customer.email)

            q.execution_options(synchronize_session="fetch")
            await self.sess.execute(q)

            return await self.get(customer_id)

    async def delete(self, customer_id: int):
        async with self.sess.begin():
            q = await self.sess.execute(select(Customer).where(Customer.id == customer_id))
            entity = q.scalars().one_or_none()
            if not entity:
                raise CustomerNotFoundError(customer_id)

            await self.sess.delete(entity)
            await self.sess.commit()

    async def get_all(self):
        async with self.sess.begin():
            query = await self.sess.execute(select(Customer))
            return query.scalars().all()

    async def get(self, customer_id: int):
        query = select(Customer).where(Customer.id == customer_id).options(selectinload(Customer.products))
        q = await self.sess.execute(query)
        entity = q.scalars().one_or_none()

        if not entity:
            raise CustomerNotFoundError(customer_id)

        return entity

    async def check(self, customer_id: int) -> bool:
        q = await self.sess.execute(select(Customer).where(Customer.id == customer_id))
        return q.scalar() is not None
