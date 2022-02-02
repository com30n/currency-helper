from typing import Any, Union

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.models import ConvertCurrencyModel, Message

router = APIRouter()


async def query_params(
    from_currency: str, to_currency: str, amount: float
) -> dict[str, Union[str, float]]:
    return {"from": from_currency, "to": to_currency, "amount": amount}


@router.get(
    "/length", response_model=ConvertCurrencyModel, responses={500: {"model": Message}}
)
async def convert(
    request: Request, q_params: Any = Depends(query_params)
) -> Union[ConvertCurrencyModel, JSONResponse]:
    try:
        response = await request.app.state.exness_client.convert_currency(
            from_currency=q_params["from"],
            to_currency=q_params["to"],
            amount=q_params["amount"],
            ctx=request,
        )
        return response
    except (ValidationError, TypeError):
        return JSONResponse(
            status_code=500, content={"message": "Coinbase returns unexpected answer"}
        )
