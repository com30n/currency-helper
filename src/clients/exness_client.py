from typing import Any

import ujson
from starlette.requests import Request

from src.clients.base_client import BaseClient
from src.models import ConvertCurrencyModel, CurrenciesModel


class ExnessClient(BaseClient):
    def __init__(self, config: dict[str, Any], *args: Any, **kwargs: Any) -> None:
        kwargs["config"] = config
        kwargs["client_name"] = "exness"
        super().__init__(*args, **kwargs)

    async def _make_graphql_query(
        self, operation_name: str, variables: dict[str, Any], query: str
    ) -> dict[str, Any]:
        params = {
            "operationName": operation_name,
            "variables": variables,
            "query": query,
        }

        headers = {"Content-Type": "application/json"}
        return await self._post_json("/", json=params, headers=headers)

    async def get_currencies_list(self, *args: Any, **kwargs: Any) -> CurrenciesModel:
        query = """
query GetConversionCurrencies {
  list: conversionMetadata {
    currencies
    __typename
  }
}"""
        json = await self._make_graphql_query("GetConversionCurrencies", {}, query)
        response_model = CurrenciesModel.parse_obj(json["data"]["list"])
        return response_model

    async def convert_currency(
        self, from_currency: str, to_currency: str, ctx: Request, amount: float = 1
    ) -> ConvertCurrencyModel:
        query = """
query GetConversionRates($from: String!, $to: String!) {
  rates: allConversionRates(from: $from, to: $to) {
  from
  to
  multiplier
  __typename
  }
}
"""
        cached_answer = await ctx.app.state.cache.get(f"{from_currency}->{to_currency}")
        if cached_answer:
            response_model = ConvertCurrencyModel(**ujson.loads(cached_answer))
        else:
            json = await self._make_graphql_query(
                "GetConversionRates", {"from": from_currency, "to": to_currency}, query
            )

            response_model = ConvertCurrencyModel.parse_obj(json["data"]["rates"][0])

            await ctx.app.state.cache.set(
                key=f"{from_currency}->{to_currency}",
                value=ujson.dumps(response_model.dict(by_alias=True)),
                expire=ctx.app.state.config["cache"]["ttl"],
            )
        response_model.amount = amount
        response_model.rate = response_model.amount * response_model.multiplier

        return response_model
