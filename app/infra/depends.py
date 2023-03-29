from dependency_injector import containers, providers

from app.repository.customer import CustomerRepository
from app.services.customer import CustomerService
from app.repository.product import ProductRepository
from app.services.product import ProductService
from app.repository.user import UserRepository
from app.services.user import UserService
from app.services.security import SecurityService
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class SSDLCContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_yaml('configs/config.yml')
    #TODO: Почему-то для pytest нужен такой путь
    config.from_yaml('./../configs/config.yml')
    engine = create_async_engine(config()['storages']['database'], future=True, echo=True)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async_session = providers.Callable(async_session_maker)

    user_repository = providers.Factory(UserRepository, sess=async_session)
    user_service = providers.Factory(UserService, user_repository=user_repository)

    customer_repository = providers.Factory(CustomerRepository, sess=async_session)
    customer_service = providers.Factory(CustomerService, customer_repository=customer_repository)

    product_repository = providers.Factory(ProductRepository, sess=async_session)
    product_service = providers.Factory(ProductService, product_repository=product_repository)

    security_service = providers.Factory(SecurityService)


