from typing import Any, AsyncGenerator, Callable, Optional, Union

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.tests.fixtures import app

app = app  # Imports optimizer fix

MOCK_PROFILE_DICT = {
    "data": {
        "list": {
            "currencies": [
                "RUB",
                "USD",
            ]
        }
    }
}


@pytest.mark.asyncio
async def test_currencies(app: Optional[Callable[..., Any]]) -> None:
    async def mocked_resp(*args: Any, **kwargs: Any) -> dict[Any, Any]:
        return MOCK_PROFILE_DICT

    app.state.exness_client._get_json = mocked_resp

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/currencies")

    print(response)
    assert response.status_code == 200
    assert "USD" in response.json()["currencies"]
    assert "RUB" in response.json()["currencies"]
