from typing import Generator
from fastapi import Depends
import asyncio
from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from repository.customer import CustomerRepository
from services.customer import CustomerService
from db_config.sqlalchemy_async_connect import SessionFactory, async_session


class TestService:
    async def process(self) -> str:
        return "testmsg"


class SSDLCContainer(containers.DeclarativeContainer):
#    wiring_config = containers.WiringConfiguration(modules=["api.customer"])
#    config = providers.Configuration()

    session_factory = SessionFactory()
    async_session = providers.Callable(async_session)
    customer_repository = providers.Singleton(CustomerRepository, session_factory=Depends(async_session))
    customer_service = providers.Factory(CustomerService, customer_repository=customer_repository)
    test_service = providers.Factory(TestService)


def get_customer_service(container: SSDLCContainer = Depends(SSDLCContainer)):
    return container.customer_service


def get_dep_str(container: SSDLCContainer = Depends(SSDLCContainer)):
    return "test3"
