from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from src import api
from src.api.v1.currencies import load_and_cache_currencies_list
from src.strategies import setup_cache_client
from src.utils.ping import ping


def setup_config(app, config: dict):
    app.config = config


def get_app(config):
    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)

    setup_cache_client(app, config)
    setup_config(app, config)

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
