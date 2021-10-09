import os
from typing import List, Optional, Dict
from urllib.parse import urljoin

import aiohttp
import aioredis
import ujson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

COINBASE_BASE_API_URI = 'https://api.coinbase.com/v2/'
COINBASE_GET_CURRENCIES_API_URI = urljoin(COINBASE_BASE_API_URI, 'currencies')
COINBASE_SPOT_API_URI = urljoin(COINBASE_BASE_API_URI, 'prices/spot?currency={currency}')

REDIS_URI = os.environ.get("REDIS_URI", "redis://localhost:6379")
# 10 minutes cache
REDIS_CACHE_TTL = 600
# 24 hours cache
REDIS_LONG_TERM_CACHE_TTL = 86400

redis = aioredis.from_url(REDIS_URI)


CURRENCIES_REDIS_KEY = 'currencies'

app = FastAPI()
def app_factory():
    pass


class CurrencyModel(BaseModel):
    id: str
    name: str
    min_size: float


class CurrenciesModel(BaseModel):
    data: List[CurrencyModel]

    def get_currencies_id(self, name: str = None) -> list:
        currencies = []
        if name:
            for currency in self.data:
                if currency.id == name:
                    currencies.append(currency.id)
                    break
        else:
            currencies = [currency.id for currency in self.data]
        return currencies


class SpotPriceModel(BaseModel):
    base: str = "BTC"
    currency: str = "USD"
    amount: float


class SpotPricesModel(BaseModel):
    data: SpotPriceModel


class Currency(BaseModel):
    name: str


async def async_request(url) -> Dict:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return await response.json()


async def load_and_cache_spot_price(currency: str = "USD") -> Optional[SpotPricesModel]:
    cached_answer = await redis.get(currency)
    if cached_answer:
        return SpotPricesModel(**ujson.loads(cached_answer))
    else:
        currencies = await load_and_cache_currencies_list()

        if currency in currencies.get_currencies_id():
            spot_prices = await async_request(COINBASE_SPOT_API_URI.format(currency=currency))
            spot_prices = SpotPricesModel(**spot_prices)
            await redis.set(currency, ujson.dumps(spot_prices.dict()), ex=REDIS_CACHE_TTL)
            return spot_prices

    return None


async def load_and_cache_currencies_list() -> CurrenciesModel:
    cached_results = await redis.get(CURRENCIES_REDIS_KEY)
    if cached_results:
        currencies_model = CurrenciesModel(**ujson.loads(cached_results))
    else:
        currencies = await async_request(COINBASE_GET_CURRENCIES_API_URI)
        currencies_model = CurrenciesModel(**currencies)
        await redis.set(CURRENCIES_REDIS_KEY, ujson.dumps(currencies_model.dict()), ex=REDIS_LONG_TERM_CACHE_TTL)
    return currencies_model


@app.on_event("startup")
async def startup_event() -> None:
    await load_and_cache_currencies_list()


@app.get("/currencies")
async def get_currency() -> CurrenciesModel:
    return await load_and_cache_currencies_list()


@app.get("/{currency}")
async def get_currency(currency: str) -> SpotPricesModel:
    currency = currency.upper()
    spot_prices = await load_and_cache_spot_price(currency)
    if not spot_prices:
        raise HTTPException(status_code=404, detail="Provided currency wasn't found")
    return spot_prices


