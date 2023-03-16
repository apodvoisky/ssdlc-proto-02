from typing import Generator
from fastapi import Depends
import asyncio
from dependency_injector import containers, providers
from dependency_injector.providers import Factory
from dependency_injector.wiring import inject, Provide

from repository.customer import CustomerRepository
from services.customer import CustomerService
from repository.product import ProductRepository
from services.product import ProductService
from db_config.sqlalchemy_async_connect import SessionFactory, async_session


class SSDLCContainer(containers.DeclarativeContainer):
#    wiring_config = containers.WiringConfiguration(modules=["api.customer"])
#    config = providers.Configuration()

    session_factory = SessionFactory()
    async_session = providers.Callable(async_session)

    customer_repository = providers.Factory(CustomerRepository, sess=async_session)
    customer_service = providers.Factory(CustomerService, customer_repository=customer_repository)

    product_repository = providers.Factory(ProductRepository, sess=async_session)
    product_service = providers.Factory(ProductService, product_repository=product_repository)
