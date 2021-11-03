import pytest
from httpx import AsyncClient

from src.tests.fixtures import app

app = app  # Imports optimizer fix

MOCK_PROFILE_DICT = {
    "data": {
        "list": {
            "currencies": [
                "AED",
                "AMD",
                "ARS",
                "AUC",
                "AUD",
                "AUX",
                "AZN",
                "BCM",
                "BDT",
                "BGN",
                "BHD",
                "BND",
                "BRL",
                "BTC",
                "BYN",
                "CAC",
                "CAD",
                "CHC",
                "CHF",
                "CLP",
                "CNH",
                "CNY",
                "COP",
                "CRC",
                "CZK",
                "DKK",
                "DZD",
                "EGP",
                "EUC",
                "EUR",
                "EUX",
                "GBC",
                "GBP",
                "GBX",
                "GEL",
                "GHS",
                "HKD",
                "HKX",
                "HRK",
                "HUF",
                "IDR",
                "ILS",
                "INR",
                "IRR",
                "ISK",
                "JOD",
                "JPX",
                "JPY",
                "KES",
                "KGS",
                "KHR",
                "KRW",
                "KWD",
                "KZT",
                "LAK",
                "LBP",
                "LKR",
                "MAD",
                "MAG",
                "MAU",
                "MBA",
                "MBB",
                "MBC",
                "MBD",
                "MMK",
                "MPD",
                "MPT",
                "MXN",
                "MYR",
                "NAD",
                "NGN",
                "NOK",
                "NPR",
                "NZD",
                "OMR",
                "PAB",
                "PEN",
                "PHP",
                "PKR",
                "PLN",
                "PYG",
                "QAR",
                "RON",
                "RUB",
                "RUR",
                "RWF",
                "SAR",
                "SCR",
                "SEK",
                "SGD",
                "SYP",
                "THB",
                "TJS",
                "TMT",
                "TND",
                "TRY",
                "TWD",
                "UAH",
                "UGX",
                "USC",
                "USD",
                "USX",
                "UYU",
                "UZS",
                "VND",
                "VUV",
                "XAF",
                "XAG",
                "XAU",
                "XOF",
                "XPD",
                "XPT",
                "ZAR",
                "ZMW",
            ]
        }
    }
}


@pytest.mark.asyncio
async def test_currencies(app):
    async def mocked_resp(*args, **kwargs):
        return MOCK_PROFILE_DICT

    app.exness_client._get_json = mocked_resp

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/fiat/currencies")

    print(response)
    assert response.status_code == 200
    assert "USD" in response.json()["currencies"]
    assert "RUB" in response.json()["currencies"]
