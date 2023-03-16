from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.data.customer import Customer

from infra.exceptions import EntityNotFoundError
from models.requests.customerreq import CustomerReqBase


class CustomerNotFoundError(EntityNotFoundError):
    entity_name: str = "Customer"


class CustomerRepository:
    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, customer: Customer):
        async with self.sess.begin():
            customer = Customer(
                first_name=customer.first_name,
                sur_name=customer.sur_name,
                second_name=customer.second_name,
                cell_phone=customer.cell_phone,
                email=customer.email)

            self.sess.add(customer)
            await self.sess.commit()

            return customer

    async def update(self, customer_id: int, customer: CustomerReqBase) -> bool:
        async with self.sess.begin():
            q = await self.sess.execute(select(Customer).where(Customer.id == customer_id))
            entity = q.scalars().one_or_none()
            if not entity:
                raise CustomerNotFoundError(customer_id)

            entity.first_name = customer.first_name
            entity.sur_name = customer.sur_name
            entity.second_name = customer.second_name
            entity.email = customer.email
            entity.cell_phone = customer.cell_phone

            await self.sess.commit()
            return entity

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
        q = await self.sess.execute(select(Customer).where(Customer.id == customer_id))
        entity = q.scalars().one_or_none()
        if not entity:
            raise CustomerNotFoundError(customer_id)

        return entity

    async def check(self, customer_id: int):
        q = await self.sess.execute(select(Customer).where(Customer.id == customer_id))
        return q.scalar()
