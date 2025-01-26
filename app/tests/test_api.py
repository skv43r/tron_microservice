from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import WalletQuery


async def test_get_wallet_info(ac: AsyncClient, session: AsyncSession):
    wallet_address = "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu"
    response = await ac.post("/wallet", params={
        "wallet_address": wallet_address
    })

    assert response.status_code == 200
    assert ("bandwidth" and "energy" and "balance") in response.json()

    query = await session.execute(
        select(WalletQuery).filter(
            WalletQuery.wallet_address == wallet_address
        ))
    assert query is not None


async def test_get_wallet_info_error(ac: AsyncClient):
    wallet_address = "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu123"
    response = await ac.post("/wallet", params={
        "wallet_address": wallet_address
    })

    assert response.status_code == 404


async def test_get_wallet_history(ac: AsyncClient):
    response = await ac.get("/history")
    assert response.status_code == 200
    assert response.json()["total"] == 4
    assert len(response.json()["items"]) == 4
    assert response.json()["items"][0]["wallet_address"] == (
        "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu"
        )
    assert response.json()["items"][1]["wallet_address"] == (
        "TMGXd47Q79NPVSRz9JvjLXzSUhqizmT7A4"
        )
    assert response.json()["items"][2]["wallet_address"] == (
        "TGkHfYXkgUgHjAKcYf3gob2rLd1N7BqRQs"
        )
    assert response.json()["items"][3]["wallet_address"] == (
        "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu"
        )


async def test_get_wallet_history_with_skip(ac: AsyncClient):
    response = await ac.get("/history", params={"skip": 1})
    assert response.status_code == 200
    assert response.json()["total"] == 4
    assert len(response.json()["items"]) == 3
    assert response.json()["items"][0]["wallet_address"] == (
        "TMGXd47Q79NPVSRz9JvjLXzSUhqizmT7A4"
    )
    assert response.json()["items"][1]["wallet_address"] == (
        "TGkHfYXkgUgHjAKcYf3gob2rLd1N7BqRQs"
    )
    assert response.json()["items"][2]["wallet_address"] == (
        "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu"
    )


async def test_get_wallet_history_with_limit(ac: AsyncClient):
    response = await ac.get("/history", params={"limit": 2})
    assert response.status_code == 200
    assert response.json()["total"] == 4
    assert len(response.json()["items"]) == 2
    assert response.json()["items"][0]["wallet_address"] == (
        "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu"
        )
    assert response.json()["items"][1]["wallet_address"] == (
        "TMGXd47Q79NPVSRz9JvjLXzSUhqizmT7A4"
        )


async def test_get_wallet_history_with_skip_and_limit(ac: AsyncClient):
    response = await ac.get("/history", params={"skip": 1, "limit": 1})
    assert response.status_code == 200
    assert response.json()["total"] == 4
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["wallet_address"] == (
        "TMGXd47Q79NPVSRz9JvjLXzSUhqizmT7A4"
        )
