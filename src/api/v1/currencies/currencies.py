from typing import Union, Set

from fastapi import APIRouter
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.models import CurrenciesModel, Message

router = APIRouter()


@router.get(
    "/currencies", response_model=Set, responses={500: {"model": Message}}
)
async def get_currencies(
        request: Request,
) -> Union[CurrenciesModel, JSONResponse]:
    try:
        return await request.app.currency_converter_client.currencies
    except (ValidationError, TypeError):
        return JSONResponse(
            status_code=500, content={"message": "Coinbase returns unexpected answer"}
        )
