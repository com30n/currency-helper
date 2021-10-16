import pytest
from httpx import AsyncClient

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
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/currencies")

    assert response.status_code == 200
    assert response.json() == MOCK_PROFILE_DICT
