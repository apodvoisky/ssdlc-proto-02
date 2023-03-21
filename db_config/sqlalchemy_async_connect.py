from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import Depends
from typing import Generator
from dependency_injector.providers import Factory

DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ssdlc02"


async def create_async_session() -> Generator:
    engine = create_async_engine(DB_URL)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        yield session


class SessionFactory(Factory):
    async_session = Factory(create_async_session)


engine = create_async_engine(DB_URL, future=True, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#engine = create_async_engine(DB_URL, future=True, echo=True)
#async_session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


# Функция, которая создает новую сессию базы данных для каждого запроса
def get_db():
    try:
        db = async_session_factory()
        yield db
    finally:
        db.close()


# Определение зависимости (dependency) для сессии базы данных
def get_db_session(db: Session = Depends(get_db)):
    return db


# Определение зависимости (dependency) для сессии базы данных
def get_db_session(db: Session = Depends(get_db)):
    return db
