from typing import List

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class CurrenciesModel(BaseModel):
    currencies: List[str]


class ConvertCurrencyModel(BaseModel):
    from_currency: str = Field(..., alias="from")
    to_currency: str = Field(..., alias="to")
    multiplier: float = 0.0
    amount: float = 0.0
    rate: float = 0.0
