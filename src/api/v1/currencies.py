from fastapi import APIRouter
from starlette.requests import Request

from src.models import CurrenciesModel

router = APIRouter()


@router.get("/currencies")
async def get_currency(request: Request) -> CurrenciesModel:
    return await request.app.coinbase_client.load_and_cache_currencies_list(ctx=request)
