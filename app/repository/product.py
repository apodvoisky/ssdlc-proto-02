from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.models.data.product import Product

from app.infra.exceptions import EntityNotFoundError
from app.models.schemas.schema import ProductCreate, ProductUpdate
from app.repository.customer import CustomerNotFoundError


class ProductNotFoundError(EntityNotFoundError):
    entity_name: str = "Product"


class ProductRepository:
    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, product: ProductCreate):
        async with self.sess.begin():
            product = Product(
                title=product.title,
                code=product.code,
                customer_id=product.customer_id,
            )

            self.sess.add(product)
            await self.sess.commit()

            return product

    async def update(self, product_id: int, product: ProductUpdate) -> bool:
        async with self.sess.begin():
            product_exists = await self.check(product_id)
            if not product_exists:
                raise ProductNotFoundError(product_id)

            q = update(Product).where(Product.id == product_id)

            if product.title:
                q = q.values(title=product.title)
            if product.code:
                q = q.values(code=product.code)
            if product.customer_id:
                q = q.values(customer_id=product.customer_id)
            q = q.values(updated_at=datetime.utcnow)

            q.execution_options(synchronize_session="fetch")

            try:
                await self.sess.execute(q)
            except IntegrityError:
                raise CustomerNotFoundError(product.customer_id)

            return await self.get(product_id)

    async def delete(self, product_id: int):
        async with self.sess.begin():
            q = await self.sess.execute(select(Product).where(Product.id == product_id))
            entity = q.scalars().one_or_none()
            if not entity:
                raise ProductNotFoundError(product_id)

            await self.sess.delete(entity)
            await self.sess.commit()

    async def get_all(self):
        async with self.sess.begin():
            query = await self.sess.execute(select(Product).options(selectinload(Product.customer)))
            return query.scalars().all()

    async def get(self, product_id: int):
        q = await self.sess.execute(select(Product).where(Product.id == product_id))
        entity = q.scalars().one_or_none()
        if not entity:
            raise ProductNotFoundError(product_id)

        return entity

    async def get_for_customer(self, customer_id: int):
        query = select(Product).where(Product.customer_id == customer_id)
        q = await self.sess.execute(query)
        entity = q.scalars().all()
        if not entity:
            raise ProductNotFoundError(customer_id)

        return entity

    async def check(self, product_id: int) -> bool:
        q = await self.sess.execute(select(Product).where(Product.id == product_id))
        return q.scalar() is not None
