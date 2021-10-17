import pytest

from src.models import CurrenciesModel
from src.tests.fixtures import app

app = app  # Imports optimizer fix

MOCK_PROFILE_DICT = {
    "data": [
        {"id": "EUR", "name": "Euro", "min_size": 0.01},
        {"id": "GBP", "name": "British Pound", "min_size": 0.01},
        {"id": "USD", "name": "US Dollar", "min_size": 0.01},
        {"id": "JPY", "name": "Japanese Yen", "min_size": 1.0},
    ]
}


@pytest.mark.asyncio
async def test_currencies(app):
    async def mocked_resp(*args, **kwargs):
        return MOCK_PROFILE_DICT

    app.coinbase_client._get = mocked_resp

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/currencies")

    assert response.status_code == 200
    assert response.json() == MOCK_PROFILE_DICT


import pytest
from httpx import AsyncClient

from src.tests.fixtures import app

app = app  # Imports optimizer fix

test_cases = [
    pytest.param(
        ["usd", "eur", "gbp", "jpy"],
        [
            [200, {"data": {"base": "BTC", "currency": "USD", "amount": 60920.49}}],
            [200, {"data": {"base": "BTC", "currency": "EUR", "amount": 52282.08}}],
            [200, {"data": {"base": "BTC", "currency": "GBP", "amount": 44134.33}}],
            [
                200,
                {"data": {"base": "BTC", "currency": "JPY", "amount": 6962914.081305}},
            ],
        ],
        id="positive_spot_prices_tests",
    ),
    pytest.param(
        ["not_existing_currency", "usd"],
        [
            [404, {"message": "Provided currency wasn't found"}, None],
            [500, {"message": "Coinbase returns unexpected answer"}, "{broken_json"],
        ],
        id="negative_spot_prices_test",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("requested,expected", test_cases)
async def test_currency(app, requested: str, expected: dict) -> None:
    async def mocked_currencies(*args, **kwargs):
        return CurrenciesModel(**MOCK_PROFILE_DICT)

    app.coinbase_client.load_and_cache_currencies_list = mocked_currencies
    for i in range(len(requested)):

        async def mocked_resp(*args, **kwargs):
            return expected[i][-1]

        app.coinbase_client._get = mocked_resp

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/{requested[i]}")

        j = response.json()
        assert response.status_code == expected[i][0]
        assert response.json() == expected[i][1]
