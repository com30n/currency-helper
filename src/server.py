from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from src import api
from src.coinbase_client import CoinbaseClient
from src.strategies import setup_cache_client
from src.utils.ping import ping


def setup_config(app, config: dict):
    app.config = config


def setup_coinbase_client(app, config: dict):
    app.coinbase_client = CoinbaseClient(config)


def get_app(config):
    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)

    setup_cache_client(app, config)
    setup_config(app, config)
    setup_coinbase_client(app, config)

    app.add_route("/-/metrics", metrics)
    app.add_route(
        "/-/ping",
        ping,
    )
    app.add_route("/health", ping)
    app.add_route("/metrics", metrics)
    app.include_router(api.v1.router, prefix="/api/v1")
    app.include_router(api.v1.router)

    return app
