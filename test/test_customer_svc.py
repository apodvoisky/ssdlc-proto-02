import asyncio
from json import dumps

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from httpx import AsyncClient

from db_config.sqlalchemy_async_connect import async_session_factory
from main import app
from models.requests.customerreq import CustomerReqBase
from repository.customer import CustomerRepository


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def atest_A():
    async with async_session_factory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            result = await repo.get_all()


@pytest.mark.asyncio
async def atest_B():
    async with async_session_factory() as sess:
        async with sess.begin():
            repo = CustomerRepository(sess)
            result = await repo.get_all()
