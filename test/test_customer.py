import pytest
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from json import dumps
from api import customer
from models.requests.customer import CustomerReq

from httpx import AsyncClient

from main import app

@pytest.mark.anyio
async def test_customer_get():
    async with AsyncClient(app=app) as ac:
        response = await ac.get("/customer")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_customer_insert():
    customer = CustomerReq(
                    id=1,
                    first_name="Петр",
                    sur_name="Иванович",
                    second_name="Сергеев",
                    cell_phone="123456",
                    email="pisergeev@test.local")

    async with AsyncClient(app=app) as ac:
        response = await ac.post(
                    "/customer",
                    content=dumps(jsonable_encoder(customer)))

    assert response.status_code == 201
