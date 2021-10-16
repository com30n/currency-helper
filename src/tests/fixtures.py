import os

import pytest
from fastapi import FastAPI

from src.coinbase_client import CoinbaseClient
from src.models import CurrenciesModel
from src.server import get_app
from src.utils.config import get_config_path, load_config


class CoinbaseClientMock(CoinbaseClient):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    async def load_and_cache_currencies_list(*args, **kwargs):
        return CurrenciesModel(
            **{
                "data": [
                    {"id": "EUR", "name": "Euro", "min_size": 0.01},
                    {"id": "GBP", "name": "British Pound", "min_size": 0.01},
                    {"id": "USD", "name": "US Dollar", "min_size": 0.01},
                    {"id": "JPY", "name": "Japanese Yen", "min_size": 1.0},
                ]
            }
        )


@pytest.fixture(scope="function")
def app() -> FastAPI:
    os.environ["CONFIG"] = "../../config.yaml"

    config_path = get_config_path()
    config = load_config(config_path)
    app = get_app(config)
    app.coinbase_client = CoinbaseClientMock(config)

    return app
