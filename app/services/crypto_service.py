"""
Модуль для работы с кошельками в сети Tron, включая получение информации
о кошельке и историю запросов.
"""

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.tron import tron
from app.models.models import WalletQuery
from app.schemas.shemas import WalletResponse, PaginatedResponse


async def wallet_info(wallet_address: str,
                      get_db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о кошельке на основе его адреса.

    - Параметры:
        - `wallet_address` (str): Адрес кошелька, для которого требуется
          информация.
        - `get_db` (AsyncSession, optional): Сессия базы данных для работы
          с таблицей `WalletQuery`.

    - Возвращает:
        `WalletResponse`: Ответ с информацией о кошельке, включая баланс,
        пропускную способность и энергию.

    - Ошибки:
        `HTTPException`: Если адрес кошелька не найден,
        вызывается ошибка 404 с описанием.
    """
    try:
        account = tron.get_account(wallet_address)
        balance = account.get("balance", 0) / 1_000_000
        bandwidth = tron.get_bandwidth(wallet_address)
        energy = account.get("energy", 0)

        wallet_query = WalletQuery(wallet_address=wallet_address)
        get_db.add(wallet_query)
        await get_db.commit()
        await get_db.refresh(wallet_query)

        return WalletResponse(bandwidth=bandwidth,
                              energy=energy,
                              balance=balance)
    except ValueError:
        raise HTTPException(status_code=404,
                            detail="Address not found")


async def wallet_history(skip: int = 0,
                         limit: int = 10,
                         get_db: AsyncSession = Depends(get_db)):
    """
    Получить историю запросов по кошелькам с пагинацией.

    - Парметры:
        - `skip` (int, optional): Сдвиг для пагинации. По умолчанию 0.
        - `limit` (int, optional): Количество записей для выборки.
           По умолчанию 10.
        - `get_db` (AsyncSession, optional): Сессия базы данных для работы
          с таблицей `WalletQuery`.

    - Возвращает:
        `PaginatedResponse`: Ответ с пагинированными результатами,
         включая общее количество записей и сам список.
    """
    result = await get_db.execute(
        select(WalletQuery).offset(skip).limit(limit)
    )
    queries = [
        {k: v for k, v in q.__dict__.items() if not k.startswith("_sa_")}
        for q in result.scalars().all()
    ]
    total_result = await get_db.execute(select(WalletQuery))
    total = len(total_result.scalars().all())
    return PaginatedResponse(total=total, items=queries)
