from typing import Optional

import ujson
from starlette.requests import Request

from src.clients.base_client import BaseClient
from src.models import CoinbaseCurrenciesModel, CoinbaseSpotPricesModel


class CoinbaseClient(BaseClient):
    def __init__(self, config, *args, **kwargs):
        self.currencies_list_cache_key = "currencies"
        super().__init__(config=config, client_name="coinbase", *args, **kwargs)

    async def load_and_cache_currencies_list(
            self,
            ctx: Request,
    ) -> CoinbaseCurrenciesModel:

        cached_results = await ctx.app.cache.get(key=self.currencies_list_cache_key)
        if cached_results:
            currencies_model = CoinbaseCurrenciesModel(**ujson.loads(cached_results))
        else:
            currencies = await self._get_json(self.client_config["currencies_api_path"])
            currencies_model = CoinbaseCurrenciesModel(**currencies)
            await ctx.app.cache.set(
                key=self.currencies_list_cache_key,
                value=ujson.dumps(currencies_model.dict()),
                expire=ctx.app.config["cache"]["long_term_ttl"],
            )
        return currencies_model

    async def load_and_cache_spot_price(
            self, ctx: Request, currency: str = "USD"
    ) -> Optional[CoinbaseSpotPricesModel]:

        cached_answer = await ctx.app.cache.get(currency)
        if cached_answer:
            return CoinbaseSpotPricesModel(**ujson.loads(cached_answer))
        else:
            currencies = await self.load_and_cache_currencies_list(ctx=ctx)

            if currency in currencies.get_currencies_id():
                spot_prices = await self._get_json(
                    self.client_config["spot_api_path"].format(currency=currency)
                )

                spot_prices = CoinbaseSpotPricesModel(**spot_prices)
                await ctx.app.cache.set(
                    key=currency,
                    value=ujson.dumps(spot_prices.dict()),
                    expire=ctx.app.config["cache"]["ttl"],
                )

                return spot_prices

        return None
