from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware

from src import api
from src.coinbase_client import CoinbaseClient
from src.strategies import setup_cache_client
from src.utils.config import get_config_path, load_config


def setup_config(app, config: dict):
    app.config = config


def setup_coinbase_client(app, config: dict):
    app.coinbase_client = CoinbaseClient(config)


def get_app():
    config_path = get_config_path()
    config = load_config(config_path)

    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)

    setup_cache_client(app, config)
    setup_config(app, config)
    setup_coinbase_client(app, config)

    app.include_router(api.router)

    return app
