from typing import Any, Callable, Optional

import pytest
from httpx import AsyncClient

from src.tests.fixtures import app

app = app  # Imports optimizer fix

MOCK_PROFILE_DICT = {
    "data": {
        "rates": [
            {
                "from": "usd",
                "to": "rub",
                "multiplier": 71.7278,
                "__typename": "ConversionRate",
            }
        ]
    }
}


@pytest.mark.asyncio
async def test_convert(app: Optional[Callable[..., Any]]) -> None:
    async def mocked_resp(*args: Any, **kwargs: Any) -> dict[Any, Any]:
        return MOCK_PROFILE_DICT

    app.state.exness_client._make_graphql_query = mocked_resp

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/convert/currency?from_currency=usd&to_currency=rub&amount=1000"
        )

    print(response)
    assert response.status_code == 200
    assert response.json() == {
        "from": "usd",
        "to": "rub",
        "multiplier": 71.7278,
        "amount": 1000,
        "rate": 71727.8,
    }
