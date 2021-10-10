from urllib.parse import urljoin

from fastapi import FastAPI
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics

import api
from src.api.v1.currencies import load_and_cache_currencies_list
from strategies import setup_cache_client


def setup_config(app, config: dict):
    app.config = config


def get_app(config):
    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)
    app.add_middleware(ContextMiddleware)

    setup_cache_client(app, config)
    setup_config(app, config)


    app.add_route("/-/metrics", metrics)
    app.include_router(api.v1.router, prefix="/api/v1")
    app.include_router(api.v1.router)

    load_and_cache_currencies_list(ctx=app)
    return app
