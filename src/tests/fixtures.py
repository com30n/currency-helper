import os
from typing import Any, AsyncGenerator, Optional

import pytest

from src.server import get_app


@pytest.mark.asyncio
@pytest.fixture(scope="function")
async def app() -> Optional[AsyncGenerator[Any, Any]]:
    os.environ["CONFIG"] = "./config.yaml"

    app = get_app()
    await app.router.startup()
    yield app
    await app.router.shutdown()
