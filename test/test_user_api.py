import uuid
from json import dumps

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.models.schemas.schema import UserCreate


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.asyncio
async def test_user_crud(base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        new_user = UserCreate(
            first_name="Антон",
            sur_name="Иванович",
            second_name="Сергеев",
            cell_phone="123456",
            email=str(uuid.uuid4()),
            password="P@User1")

        response = await ac.post(
                    "/users",
                    content=dumps(jsonable_encoder(new_user)))

        assert response.status_code == 201

        user_id = str(response.json()["id"])
        response = await ac.get(
            f"/users/{user_id}")

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_get_404(base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        fake_user_id = str(uuid.uuid4())
        response = await ac.get(
            f"/users/{fake_user_id}")

        assert response.status_code == 404
