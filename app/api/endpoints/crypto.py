"""
Модуль для работы с криптовалютными кошельками.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.shemas import WalletResponse, PaginatedResponse
from app.services.crypto_service import wallet_info, wallet_history

crypto_router = APIRouter()


@crypto_router.post("/wallet",
                    response_model=WalletResponse,
                    tags=["crypto"])
async def get_wallet_info(wallet_address: str,
                          get_db: AsyncSession = Depends(get_db)):
    """
    Получить информацию о криптовалютном кошельке.

    - Параметры:
        - `wallet_address` (str): Адрес кошелька,
        информацию о котором нужно получить.

    - Ответ:
        - Возвращает объект `WalletResponse`, содержащий данные о кошельке,
          такие как баланс, пропускная способность и энергия.

    - Ошибки:
        - 404: Ошибка валидации (например, некорректный формат адреса).
        - 500: Ошибка сервера.
    """
    return await wallet_info(wallet_address, get_db)


@crypto_router.get("/history",
                   response_model=PaginatedResponse,
                   tags=["crypto"])
async def get_wallet_history(skip: int = 0,
                             limit: int = 10,
                             get_db: AsyncSession = Depends(get_db)):
    """
    Получить историю запростов кошельков.

    - Параметры:
        - `skip` (int): Количество записей для пропуска (по умолчанию 0).
        - `limit` (int): Максимальное количество записей для возврата
          (по умолчанию 10).

    - Ответ:
        - Возвращает объект `PaginatedResponse`,
        содержащий общее количество записей и сам список.

    - Ошибки:
        - 500: Ошибка сервера.
    """
    return await wallet_history(skip, limit, get_db)
