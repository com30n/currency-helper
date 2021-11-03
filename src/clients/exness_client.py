from src.clients.base_client import BaseClient
from src.models import CurrenciesModel


class ExnessClient(BaseClient):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config=config, client_name="exness", *args, **kwargs)

    async def get_currencies_list(self, *args, **kwargs) -> CurrenciesModel:
        query = """
query GetConversionCurrencies {
  list: conversionMetadata {
    currencies
    __typename
  }
}"""
        params = {
            "operationName": "GetConversionCurrencies",
            "variables": {},
            "query": query,
        }
        headers = {"Content-Type": "application/json"}
        json = await self._post_json("/", json=params, headers=headers)
        response_model = CurrenciesModel.parse_obj(json["data"]["list"])
        return response_model
