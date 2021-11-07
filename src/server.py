from functools import partial
from typing import Any, Callable, List

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware

from src import api
from src.clients.exness_client import ExnessClient
from src.strategies import close_cache_client, setup_cache_client
from src.utils.config import get_config_path, load_config


def setup_config(app: FastAPI, config: dict[str, Any]) -> None:
    app.state.config = config


def setup_exness_client(app: FastAPI, config: dict[str, Any]) -> None:
    app.state.exness_client = ExnessClient(config)


def close_config(app: FastAPI, config: dict[str, Any]) -> None:
    pass


async def close_exness_client(app: FastAPI, config: dict[str, Any]) -> None:
    await app.state.exness_client.close()


def _on_event(
    func_list: List[Callable[..., None]],
    app: FastAPI,
    config: dict[str, Any],
) -> List[Callable[[None], None]]:
    return [partial(func, app=app, config=config) for func in func_list]


def on_startup(app: FastAPI, config: dict[str, Any]) -> List[Callable[[None], None]]:
    return _on_event(
        func_list=[setup_cache_client, setup_config, setup_exness_client],
        app=app,
        config=config,
    )


def on_shutdown(app: FastAPI, config: dict[str, Any]) -> List[Callable[[None], None]]:
    return _on_event(
        func_list=[close_cache_client, close_config, close_exness_client],  # type: ignore
        app=app,
        config=config,
    )


def get_app() -> FastAPI:
    config_path = get_config_path()
    config = load_config(config_path)

    app = FastAPI()
    app.add_middleware(PrometheusMiddleware)

    app.router.on_startup = on_startup(app, config)
    app.router.on_shutdown = on_shutdown(app, config)

    app.include_router(api.router)

    return app
