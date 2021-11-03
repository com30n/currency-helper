from typing import Union, List

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.models import Message, ConvertCurrencyModel

router = APIRouter()


async def query_params(from_currency: str, to_currency: str, amount: float) -> dict:
    return {"from": from_currency, "to": to_currency, "amount": amount}


@router.get(
    "/", response_model=ConvertCurrencyModel, responses={500: {"model": Message}}
)
async def convert(
        request: Request,
        q_params=Depends(query_params)
) -> Union[ConvertCurrencyModel, JSONResponse]:
    try:
        response = await request.app.exness_client.convert_currency(
            from_currency=q_params["from"],
            to_currency=q_params["to"],
            amount=q_params["amount"],
            ctx=request
        )
        return response
    except (ValidationError, TypeError) as e:
        return JSONResponse(
            status_code=500, content={"message": "Coinbase returns unexpected answer"}
        )
