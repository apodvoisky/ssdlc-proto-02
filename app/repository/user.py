from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.data.user import User
from app.models.schemas.schema import UserCreate, UserUpdate

from app.infra.exceptions import UserEmailAlreadyExists, UserNotFoundError



class UserRepository:
    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, data: UserCreate):
        async with self.sess.begin():
            user = User(
                first_name=data.first_name,
                sur_name=data.sur_name,
                second_name=data.second_name,
                cell_phone=data.cell_phone,
                email=data.email,
                password=data.password)

            self.sess.add(user)
            try:
                await self.sess.commit()
            except IntegrityError as e:
                if -1 != str(e).find("user_email_key"):
                    raise UserEmailAlreadyExists()

            return user

    async def update(self, user_id: int, user: UserUpdate) -> bool:
        async with self.sess.begin():
            user_exists = await self.check(user_id)
            if not user_exists:
                raise UserNotFoundError(user_id)

            q = update(User).where(User.id == user_id)

            if user.first_name:
                q = q.values(first_name=user.first_name)
            if user.sur_name:
                q = q.values(sur_name=user.sur_name)
            if user.second_name:
                q = q.values(second_name=user.second_name)
            if user.cell_phone:
                q = q.values(cell_phone=user.cell_phone)
            if user.email:
                q = q.values(email=user.email)
            q = q.values(updated_at=datetime.utcnow)

            q.execution_options(synchronize_session="fetch")
            await self.sess.execute(q)

            return await self.get(user_id)

    async def delete(self, user_id: int):
        async with self.sess.begin():
            q = await self.sess.execute(select(User).where(User.id == user_id))
            entity = q.scalars().one_or_none()
            if not entity:
                raise UserNotFoundError(user_id)

            await self.sess.delete(entity)
            await self.sess.commit()

    async def get_all(self):
        async with self.sess.begin():
            query = await self.sess.execute(select(User))
            return query.scalars().all()

    async def get(self, user_id: int):
        query = select(User).where(User.id == user_id)
        q = await self.sess.execute(query)
        entity = q.scalars().one_or_none()

        if not entity:
            raise UserNotFoundError(user_id)

        return entity

    async def get_by_email(self, email: str):
        query = select(User).where(User.email == email)
        q = await self.sess.execute(query)
        entity = q.scalars().one_or_none()

        if not entity:
            raise UserNotFoundError(email)

        return entity

    async def check(self, user_id: int) -> bool:
        q = await self.sess.execute(select(User).where(User.id == user_id))
        return q.scalar() is not None
