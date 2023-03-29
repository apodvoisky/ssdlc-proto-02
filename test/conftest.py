import pytest
import sys
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _database_url():
    return "postgresql+asyncpg://postgres:postgres@localhost/dbtest"


@pytest.fixture(scope="session")
def init_database():
    from app.infra.base import Base

    return Base.metadata.create_all()

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000/"
