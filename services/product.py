from repository.product import ProductRepository
from models.schemas.schema import ProductBase, ProductUpdate, ProductCreate


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_all(self):
        products = await self.product_repository.get_all()
        return products

    async def get(self, product_id: int):
        product = await self.product_repository.get(product_id)
        return product

    async def create(self, product: ProductCreate):
        return await self.product_repository.insert(product)
    
    async def delete(self, product_id: int):
        return await self.product_repository.delete(product_id)

    async def update(self, product_id: int, product: ProductUpdate):
        return await self.product_repository.update(product_id, product)

    async def get_customer_products(self, customer_id: int):
        return await self.product_repository.get_for_customer(customer_id)
