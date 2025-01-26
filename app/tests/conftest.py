import json
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert
from app.core.config import settings
from app.core.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.models.models import WalletQuery


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    wallets = open_mock_json("wallets")

    async with async_session_maker() as session:
        add_wallets = insert(WalletQuery).values(wallets)

        await session.execute(add_wallets)
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://testserver",
                           transport=ASGITransport(fastapi_app)) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
