from typing import Optional
from urllib.parse import urljoin

import ujson
from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from src.api.v1.currencies import load_and_cache_currencies_list
from src.models import SpotPricesModel
from src.utils.requests import async_request

router = APIRouter()


async def load_and_cache_spot_price(
    ctx: Request, currency: str = "USD"
) -> Optional[SpotPricesModel]:
    COINBASE_SPOT_API_URI = urljoin(
        ctx.app.config["coinbase"]["base_api_url"],
        ctx.app.config["coinbase"]["spot_api_path"],
    )

    cached_answer = await ctx.app.cache.get(currency)
    if cached_answer:
        return SpotPricesModel(**ujson.loads(cached_answer))
    else:
        currencies = await load_and_cache_currencies_list(ctx=ctx)

        if currency in currencies.get_currencies_id():
            spot_prices = await async_request(
                COINBASE_SPOT_API_URI.format(currency=currency)
            )
            spot_prices = SpotPricesModel(**spot_prices)
            await ctx.app.cache.set(
                key=currency,
                value=ujson.dumps(spot_prices.dict()),
                expire=ctx.app.config["cache"]["ttl"],
            )

            return spot_prices

    return None


@router.get("/{currency}")
async def get_currency(request: Request, currency: str) -> SpotPricesModel:
    currency = currency.upper()
    spot_prices = await load_and_cache_spot_price(ctx=request, currency=currency)
    if not spot_prices:
        raise HTTPException(status_code=404, detail="Provided currency wasn't found")
    return spot_prices
