from typing import List

from pydantic import BaseModel


class CurrencyModel(BaseModel):
    id: str
    name: str
    min_size: float


class CurrenciesModel(BaseModel):
    data: List[CurrencyModel]

    def get_currencies_id(self, name: str = None) -> list:
        currencies = []
        if name:
            for currency in self.data:
                if currency.id == name:
                    currencies.append(currency.id)
                    break
        else:
            currencies = [currency.id for currency in self.data]
        return currencies


class SpotPriceModel(BaseModel):
    base: str = "BTC"
    currency: str = "USD"
    amount: float


class SpotPricesModel(BaseModel):
    data: SpotPriceModel


class Currency(BaseModel):
    name: str


class Message(BaseModel):
    message: str
