from typing import Union

from fastapi import APIRouter
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.models import CurrenciesModel, Message

router = APIRouter()


@router.get(
    "/currencies",
    response_model=CurrenciesModel,
    responses={
        500: {
            "model": Message
        }
    }
)
async def get_currency(
        request: Request,
) -> Union[CurrenciesModel, JSONResponse]:
    try:
        return request.app.coinbase_client.load_and_cache_currencies_list(ctx=request)
    except (ValidationError, TypeError):
        return JSONResponse(status_code=500, content={"message": "Coinbase returns unexpected answer"})
