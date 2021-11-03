from typing import Union

from fastapi import APIRouter
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.models import CoinbaseCurrenciesModel, Message

router = APIRouter()


@router.get(
    "/currencies",
    response_model=CoinbaseCurrenciesModel,
    responses={500: {"model": Message}},
)
async def get_currencies(
    request: Request,
) -> Union[CoinbaseCurrenciesModel, JSONResponse]:
    try:
        return await request.app.coinbase_client.load_and_cache_currencies_list(
            ctx=request
        )
    except (ValidationError, TypeError):
        return JSONResponse(
            status_code=500, content={"message": "Coinbase returns unexpected answer"}
        )
