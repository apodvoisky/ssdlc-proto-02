from datetime import datetime
from typing import Dict, Any

from sqlalchemy import update, delete, insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.data.customer import Customer
from db_config.sqlalchemy_async_connect import SessionFactory

class CustomerRepository:

    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, customer: Customer) -> bool:
        try:
            sql = insert(Customer).values(first_name=customer.first_name,
                                          sur_name=customer.sur_name,
                                          second_name=customer.second_name,
                                          cell_phone=customer.cell_phone,
                                          email=customer.email)
            #sql.execution_options(synchronize_session="fetch")
            #await self.sess.execute(sql)

            self.session_factory.add(customer)
            await self.session_factory.flush()
        except Exception as e:
            return {"result": False, "message": e}

        return {"result": True, "message": "OK"}

    async def update(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            details["timeout"] = datetime.strptime(details["timeout"], "%H:%M")
            details["timein"] = datetime.strptime(details["timein"], "%H:%M")
            sql = update(Customer).where(Customer.id == id).values(**details)
            sql.execution_options(synchronize_session="fetch")
            await self.session_factory.execute(sql)

        except:
            return False
        return True

    async def delete(self, id: int) -> bool:
        try:
            sql = delete(Customer).where(Customer.id == id)
            sql.execution_options(synchronize_session="fetch")
            await self.session_factory.execute(sql)
        except:
            return False
        return True

    async def get_all(self):
        async with self.sess.begin():
            query = await self.sess.execute(select(Customer))
            return query.scalars().all()

    async def get(self, id: int):
        q = await self.session_factory.execute(select(Customer).where(Customer.id == id))
        return q.scalars().all()

    async def check(self, id: int):
        q = await self.session_factory.execute(select(Customer).where(Customer.id == id))
        return q.scalar()
