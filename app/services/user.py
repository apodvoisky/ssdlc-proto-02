from app.repository.user import UserRepository
from app.models.schemas.schema import UserCreate, UserUpdate
from app.infra.hashservice import HashService

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all(self):
        users = await self.user_repository.get_all()
        return users

    async def get(self, user_id: int):
        user = await self.user_repository.get(user_id)
        return user

    async def create(self, user: UserCreate):
        user.password = HashService.get_password_hash(user.password)
        return await self.user_repository.insert(user)

    async def delete(self, user_id: int):
        return await self.user_repository.delete(user_id)

    async def update(self, user_id: int, user: UserUpdate):
        return await self.user_repository.update(user_id, user)

    async def get_by_email(self, email: str):
        return await self.user_repository.get_by_email(email)
