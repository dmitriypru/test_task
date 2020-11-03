from fastapi import APIRouter

from app.routers import rates

api_router = APIRouter()


api_router.include_router(rates.router, prefix='/rates', tags=['Rates'])
