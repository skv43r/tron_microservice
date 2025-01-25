from fastapi import FastAPI
from app.api.endpoints.crypto import crypto_router as tron_router

app = FastAPI(
    title="Tron API",
    description="API для взаимодействия с блокчейном Tron"
)

app.include_router(tron_router)