from json import dumps

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.models.schemas.schema import CustomerBase


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_customer_get():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        new_customer = CustomerBase(
            first_name="Антон",
            sur_name="Иванович",
            second_name="Сергеев",
            cell_phone="123456",
            email="pisergeev@test.local")

        response = await ac.post(
                    "/customer",
                    content=dumps(jsonable_encoder(new_customer)))

    assert response.status_code == 201

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        response = await ac.get("/customer")
        assert response.status_code == 200

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        response = await ac.get("/customer/10")
        assert response.status_code == 200
