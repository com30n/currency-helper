from typing import Any, Type, TypeVar

from fastapi import FastAPI

CacheMockType = TypeVar("CacheMockType", bound="CacheMock")


class CacheMock:
    @staticmethod
    async def set(*args: Any, **kwargs: Any) -> None:
        pass

    @staticmethod
    async def get(*args: Any, **kwargs: Any) -> None:
        pass

    @classmethod
    def setup(cls: Type[CacheMockType]) -> Type[CacheMockType]:
        return cls

    @staticmethod
    def close() -> None:
        pass


def init_cache_client(app: FastAPI, config: dict[str, Any]) -> None:
    app.state.cache = CacheMock.setup()


def close_cache_client(app: FastAPI, config: dict[str, Any]) -> None:
    app.state.cache.close()
