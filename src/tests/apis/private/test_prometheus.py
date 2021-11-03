import pytest
from httpx import AsyncClient

from src.tests.fixtures import app

app = app  # Imports optimizer fix


@pytest.mark.asyncio
async def test_currency(app) -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/-/metrics")

    assert response.status_code == 200
    assert response.text is not None
