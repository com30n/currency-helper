from currency_converter import CurrencyConverter
from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware

from src import api
from src.coinbase_client import CoinbaseClient
from src.strategies import setup_cache_client
from src.utils.config import get_config_path, load_config


def setup_config(app: FastAPI, config: dict):
    app.config = config


def setup_coinbase_client(app: FastAPI, config: dict):
    app.coinbase_client = CoinbaseClient(config)


def setup_currency_converter_client(app: FastAPI, config: dict):
    cc_conf = config.get("currency_converter", {})
    app.currency_converter_client = CurrencyConverter(
        fallback_on_missing_rate_method=cc_conf.get("fallback_on_missing_rate_method", "last_known"),
        fallback_on_wrong_date=cc_conf.get(bool("fallback_on_wrong_date"), True),
        decimal=cc_conf.get(bool("decimal"), True)
    )


def get_app():
    config_path = get_config_path()
    config = load_config(config_path)

    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)

    setup_cache_client(app, config)
    setup_config(app, config)
    setup_coinbase_client(app, config)
    setup_currency_converter_client(app, config)

    app.include_router(api.router)

    return app
