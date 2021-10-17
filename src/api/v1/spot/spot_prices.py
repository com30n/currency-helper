from typing import Union

from fastapi import APIRouter
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.models import Message, SpotPricesModel

router = APIRouter()


@router.get(
    "/{currency}",
    response_model=SpotPricesModel,
    responses={500: {"model": Message}, 404: {"model": Message}},
)
async def get_currency(
    request: Request, currency: str
) -> Union[SpotPricesModel, JSONResponse]:
    currency = currency.upper()
    try:
        spot_prices = await request.app.coinbase_client.load_and_cache_spot_price(
            ctx=request, currency=currency
        )
    except (ValidationError, TypeError):
        return JSONResponse(
            status_code=500, content={"message": "Coinbase returns unexpected answer"}
        )
    if not spot_prices:
        return JSONResponse(
            status_code=404, content={"message": "Provided currency wasn't found"}
        )

    return spot_prices
