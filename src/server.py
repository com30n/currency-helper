from functools import partial

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware

from src import api
from src.clients.exness_client import ExnessClient
from src.strategies import close_cache_client, setup_cache_client
from src.utils.config import get_config_path, load_config


def setup_config(app: FastAPI, config: dict):
    app.config = config


def setup_exness_client(app: FastAPI, config: dict):
    app.exness_client = ExnessClient(config)


def close_config(app: FastAPI, config: dict):
    pass


async def close_exness_client(app: FastAPI, config: dict):
    await app.exness_client.close()


def _on_event(func_list, app, config):
    return [partial(func, app=app, config=config) for func in func_list]


def on_startup(app, config):
    return _on_event(
        func_list=[setup_cache_client, setup_config, setup_exness_client],
        app=app,
        config=config,
    )


def on_shutdown(app, config):
    return _on_event(
        func_list=[close_cache_client, close_config, close_exness_client],
        app=app,
        config=config,
    )


def get_app():
    config_path = get_config_path()
    config = load_config(config_path)

    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)

    app.router.on_startup = on_startup(app, config)
    app.router.on_shutdown = on_shutdown(app, config)

    app.include_router(api.router)

    return app
