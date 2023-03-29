import sys
import uuid

import pytest


from app.main import app
from app.models.schemas.schema import CustomerBase, UserCreate
from app.infra.depends import SSDLCContainer

from app.infra.exceptions import UserEmailAlreadyExists


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.asyncio
async def test_user_create():
    user_service = SSDLCContainer.user_service()
    user1 = await user_service.create(user=UserCreate(
        first_name="User1",
        second_name="User1",
        sur_name="User1",
        cell_phone="User1",
        email=str(uuid.uuid4()),
        password="P@User1"
    ))

    assert user1 is not None


@pytest.mark.asyncio
async def test_user_duplicate_emails():
    user_service = SSDLCContainer.user_service()

    with pytest.raises(UserEmailAlreadyExists):
        await user_service.create(user=UserCreate(
            first_name="User1",
            second_name="User1",
            sur_name="User1",
            cell_phone="User1",
            email="test@email.ru",
            password="P@User1"
        ))
        await user_service.create(user=UserCreate(
            first_name="User1",
            second_name="User1",
            sur_name="User1",
            cell_phone="User1",
            email="test@email.ru",
            password="P@User1"
        ))



container = SSDLCContainer()
container.wire(modules=[sys.modules[__name__]])
