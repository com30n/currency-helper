import os

import pytest
from fastapi import FastAPI

from src.server import get_app
from src.utils.config import get_config_path, load_config


@pytest.fixture(scope="function")
def app() -> FastAPI:
    os.environ["CONFIG"] = "./config.yaml"

    config_path = get_config_path()
    config = load_config(config_path)
    app = get_app(config)

    return app
