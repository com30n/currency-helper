from typing import List

from pydantic import BaseModel


class CoinbaseCurrencyModel(BaseModel):
    id: str
    name: str
    min_size: float


class CoinbaseCurrenciesModel(BaseModel):
    data: List[CoinbaseCurrencyModel]

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


class CoinbaseSpotPriceModel(BaseModel):
    base: str = "BTC"
    currency: str = "USD"
    amount: float


class CoinbaseSpotPricesModel(BaseModel):
    data: CoinbaseSpotPriceModel


class Message(BaseModel):
    message: str


class CurrenciesModel(BaseModel):
    currencies: List[str]
