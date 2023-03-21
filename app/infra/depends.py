from dependency_injector import containers, providers

from app.repository.customer import CustomerRepository
from app.services.customer import CustomerService
from app.repository.product import ProductRepository
from app.services.product import ProductService
from app.db_config.sqlalchemy_async_connect import SessionFactory, async_session


class SSDLCContainer(containers.DeclarativeContainer):
#    wiring_config = containers.WiringConfiguration(modules=["api.customer"])
#    config = providers.Configuration()

    session_factory = SessionFactory()
    async_session = providers.Callable(async_session)

    customer_repository = providers.Factory(CustomerRepository, sess=async_session)
    customer_service = providers.Factory(CustomerService, customer_repository=customer_repository)

    product_repository = providers.Factory(ProductRepository, sess=async_session)
    product_service = providers.Factory(ProductService, product_repository=product_repository)
