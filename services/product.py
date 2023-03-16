from repository.product import ProductRepository
from models.schemas.schema import ProductReqBase


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_all(self):
        products = await self.product_repository.get_all()
        return products

    async def get(self, product_id: int):
        product = await self.product_repository.get(product_id)
        return product

    async def create(self, product: ProductReqBase):
        return await self.product_repository.insert(product)
    
    async def delete(self, product_id: int):
        return await self.product_repository.delete(product_id)

    async def update(self, product_id: int, product: ProductReqBase):
        return await self.product_repository.update(product_id, product)
