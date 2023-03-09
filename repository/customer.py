from typing import Dict, Any

from sqlalchemy import update, delete, insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from models.data.customer import Customer
from datetime import datetime


class CustomerRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    async def insert(self, customer: Customer) -> bool:
        try:
            sql = insert(Customer).values(id=customer.id, member_id=customer.member_id,
                                          timein=datetime.strptime(customer.timein, "%H:%M"),
                                          timeout=datetime.strptime(customer.timeout, "%H:%M"),
                                          date_log=customer.date_log)
            sql.execution_options(synchronize_session="fetch")
            await self.sess.execute(sql)

            # self.sess.add(customer)
            # await self.sess.flush()
        except:
            return False
        return True

    async def update(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            details["timeout"] = datetime.strptime(details["timeout"], "%H:%M")
            details["timein"] = datetime.strptime(details["timein"], "%H:%M")
            sql = update(Customer).where(Customer.id == id).values(**details)
            sql.execution_options(synchronize_session="fetch")
            await self.sess.execute(sql)

        except:
            return False
        return True

    async def delete(self, id: int) -> bool:
        try:
            sql = delete(Customer).where(Customer.id == id)
            sql.execution_options(synchronize_session="fetch")
            await self.sess.execute(sql)
        except:
            return False
        return True

    async def get_all(self):
        q = await self.sess.execute(select(Customer))
        return q.scalars().all()

    async def get(self, id: int):
        q = await self.sess.execute(select(Customer).where(Customer.member_id == id))
        return q.scalars().all()

    async def check(self, id: int):
        q = await self.sess.execute(select(Customer).where(Customer.id == id))
        return q.scalar()
