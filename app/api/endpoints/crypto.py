from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.shemas import WalletResponse, PaginatedResponse
from app.services.crypto_service import wallet_info, wallet_history

crypto_router = APIRouter()

@crypto_router.post("/wallet", response_model=WalletResponse, tags=["crypto"], description="Получить информацию о кошельке")
async def get_wallet_info(wallet_address: str, get_db: AsyncSession = Depends(get_db)):
    return await wallet_info(wallet_address, get_db)

@crypto_router.get("/history", response_model=PaginatedResponse, tags=["crypto"], description="Получить историю кошелька")
async def get_wallet_history(skip: int = 0, limit: int = 10, get_db: AsyncSession = Depends(get_db)):
    return await wallet_history(skip, limit, get_db)