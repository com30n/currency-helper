from urllib.parse import urljoin

import ujson
from fastapi import APIRouter
from starlette.requests import Request

from src.models import CurrenciesModel
from src.utils.requests import async_request

router = APIRouter()

CURRENCIES_LIST_CACHE_KEY = "currencies"


async def load_and_cache_currencies_list(ctx: Request) -> CurrenciesModel:
    COINBASE_GET_CURRENCIES_API_URI = urljoin(
        ctx.app.config["coinbase"]["base_api_url"],
        ctx.app.config["coinbase"]["currencies_api_path"],
    )

    cached_results = await ctx.app.cache.get(key=CURRENCIES_LIST_CACHE_KEY)
    if cached_results:
        currencies_model = CurrenciesModel(**ujson.loads(cached_results))
    else:
        currencies = await async_request(COINBASE_GET_CURRENCIES_API_URI)
        currencies_model = CurrenciesModel(**currencies)
        await ctx.app.cache.set(
            key=CURRENCIES_LIST_CACHE_KEY,
            value=ujson.dumps(currencies_model.dict()),
            expire=ctx.app.config["cache"]["long_term_ttl"],
        )
    return currencies_model


@router.get("/currencies")
async def get_currency(request: Request) -> CurrenciesModel:
    return await load_and_cache_currencies_list(ctx=request)
