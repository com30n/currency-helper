import os

import pytest
from fastapi import FastAPI

from src.server import get_app


@pytest.fixture(scope="function")
def app() -> FastAPI:
    os.environ["CONFIG"] = "./config.yaml"

    app = get_app()

    return app
