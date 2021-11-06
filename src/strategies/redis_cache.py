from typing import Any, Type

from cashews import cache
from fastapi import FastAPI


def init_cache_client(app: FastAPI, config: dict[str, Any]) -> None:
    app.state.cache = cache.setup(config["cache"]["redis"]["uri"])


def close_cache_client(app: FastAPI, config: dict[str, Any]) -> None:
    app.state.cache.close()
