from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from src.models import SpotPricesModel

router = APIRouter()


@router.get("/{currency}")
async def get_currency(request: Request, currency: str) -> SpotPricesModel:
    currency = currency.upper()
    try:
        spot_prices = await request.app.coinbase_client.load_and_cache_spot_price(
            ctx=request, currency=currency
        )
    except (ValidationError, TypeError):
        raise HTTPException(status_code=500, detail="Coinbase returns invalid answer")
    if not spot_prices:
        raise HTTPException(status_code=404, detail="Provided currency wasn't found")

    return spot_prices
