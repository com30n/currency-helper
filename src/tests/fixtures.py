import os

import pytest
from fastapi import FastAPI

from src.server import get_app

# @pytest.yield_fixture(scope="module")
# def event_loop(request):
#     import asyncio
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def app() -> FastAPI:
    os.environ["CONFIG"] = "./config.yaml"

    app = get_app()
    await app.router.startup()
    yield app
    await app.router.shutdown()


# @pytest.fixture(scope="session", autouse=True)
# @pytest.mark.asyncio
# async def cleanup(app):
#     """Cleanup a testing directory once we are finished."""
#     await app.router.shutdown()
