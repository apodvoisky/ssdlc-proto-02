from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.data.product import Product

from infra.exceptions import EntityNotFoundError
from models.schemas.schema import ProductReqBase


class ProductNotFoundError(EntityNotFoundError):
    entity_name: str = "Product"


class ProductRepository:
    def __init__(self, sess: AsyncSession):
        self.sess: AsyncSession = sess

    async def insert(self, product: Product):
        async with self.sess.begin():
            product = Product(
                title=product.title,
                code=product.code)

            self.sess.add(product)
            await self.sess.commit()

            return product

    async def update(self, product_id: int, product: ProductReqBase) -> bool:
        async with self.sess.begin():
            q = await self.sess.execute(select(Product).where(Product.id == product_id))
            entity = q.scalars().one_or_none()
            if not entity:
                raise ProductNotFoundError(product_id)

            entity.title = product.title
            entity.code = product.code

            await self.sess.commit()
            return entity

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
            query = await self.sess.execute(select(Product))
            return query.scalars().all()

    async def get(self, product_id: int):
        q = await self.sess.execute(select(Product).where(Product.id == product_id))
        entity = q.scalars().one_or_none()
        if not entity:
            raise ProductNotFoundError(product_id)

        return entity

    async def check(self, product_id: int):
        q = await self.sess.execute(select(Product).where(Product.id == product_id))
        return q.scalar()
