"""
A decorator to parse query params into pydantic model
https://github.com/tiangolo/fastapi/issues/318
"""

from typing import Type

from pydantic.main import BaseModel
from starlette.requests import Request


def as_query(cls: Type[BaseModel]):
    def as_query_func(request: Request):
        return cls(**request.query_params)

    setattr(cls, "as_query", as_query_func)
    return cls
