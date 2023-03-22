from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.data.customer import Customer
from app.infra.exceptions import EntityNotFoundError
from app.models.schemas.schema import CustomerCreate, CustomerUpdate


class CustomerNotFoundError(EntityNotFoundError):
    entity_name: str = "Customer"


class CustomerRepository:
    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, data: CustomerCreate):
        async with self.sess.begin():
            customer = Customer(
                full_name=data.full_name,
                short_name=data.short_name,
                primary_contact=data.primary_contact,
                secondary_contact=data.secondary_contact,
            )

            self.sess.add(customer)
            await self.sess.commit()

            return customer

    async def update(self, customer_id: int, customer: CustomerUpdate) -> bool:
        async with self.sess.begin():
            customer_exists = await self.check(customer_id)
            if not customer_exists:
                raise CustomerNotFoundError(customer_id)

            q = update(Customer).where(Customer.id == customer_id)

            if customer.full_name:
                q = q.values(full_name=customer.full_name)
            if customer.short_name:
                q = q.values(short_name=customer.short_name)
            if customer.primary_contact:
                q = q.values(second_name=customer.primary_contact)
            if customer.secondary_contact:
                q = q.values(cell_phone=customer.secondary_contact)

            q = q.values(updated_at=datetime.utcnow)

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
