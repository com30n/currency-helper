from typing import Optional
from urllib.parse import urljoin

import aiohttp
import ujson
from pydantic import ValidationError
from starlette.requests import Request

from src.models import CurrenciesModel, SpotPricesModel


class CoinbaseClient:
    def __init__(self, config, *args, **kwargs):
        self.config = config
        self._timeout = config.get("timeout", 10)
        self.session = aiohttp.ClientSession(
            json_serialize=ujson.dumps,
            timeout=aiohttp.client.ClientTimeout(total=self._timeout),
        )
        self.currencies_list_cache_key = "currencies"
        self.session = None

    async def _get(self, url) -> dict:
        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        async with self.session.get(url) as resp:
            return await resp.json()

    async def load_and_cache_currencies_list(
        self,
        ctx: Request,
    ) -> CurrenciesModel:
        coinbase_get_currencies_api_uri = urljoin(
            self.config["coinbase"]["base_api_url"],
            self.config["coinbase"]["currencies_api_path"],
        )

        cached_results = await ctx.app.cache.get(key=self.currencies_list_cache_key)
        if cached_results:
            currencies_model = CurrenciesModel(**ujson.loads(cached_results))
        else:
            currencies = await self._get(coinbase_get_currencies_api_uri)
            currencies_model = CurrenciesModel(**currencies)
            await ctx.app.cache.set(
                key=self.currencies_list_cache_key,
                value=ujson.dumps(currencies_model.dict()),
                expire=ctx.app.config["cache"]["long_term_ttl"],
            )
        return currencies_model

    async def load_and_cache_spot_price(
        self, ctx: Request, currency: str = "USD"
    ) -> Optional[SpotPricesModel]:
        coinbase_spot_api_uri = urljoin(
            self.config["coinbase"]["base_api_url"],
            self.config["coinbase"]["spot_api_path"],
        )

        cached_answer = await ctx.app.cache.get(currency)
        if cached_answer:
            return SpotPricesModel(**ujson.loads(cached_answer))
        else:
            currencies = await self.load_and_cache_currencies_list(ctx=ctx)

            if currency in currencies.get_currencies_id():
                spot_prices = await self._get(
                    coinbase_spot_api_uri.format(currency=currency)
                )

                spot_prices = SpotPricesModel(**spot_prices)
                await ctx.app.cache.set(
                    key=currency,
                    value=ujson.dumps(spot_prices.dict()),
                    expire=ctx.app.config["cache"]["ttl"],
                )

                return spot_prices

        return None

    async def close(self):
        await self.session.close()
