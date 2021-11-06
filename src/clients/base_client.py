from enum import Enum
from typing import Any, List
from urllib.parse import urljoin

import aiohttp
import ujson


class HttpMethod(Enum):
    get = "get"
    post = "post"
    put = "put"
    options = "options"


class BaseClient:
    def __init__(
        self, config: dict[str, Any], client_name: str, *args: List[Any], **kwargs: Any
    ) -> None:
        self.config = config
        self.client_config = config["clients"][client_name]
        self.base_url = self.client_config["base_url"]
        self._timeout = self.client_config.get("timeout", kwargs.get("timeout", 10))
        self.session = aiohttp.ClientSession(
            json_serialize=ujson.dumps,
            timeout=aiohttp.client.ClientTimeout(total=self._timeout),
        )
        self.currencies_list_cache_key = client_name

    async def _request(self, api_path: str, method: HttpMethod, **kwargs: Any) -> str:
        url = urljoin(self.base_url, api_path)

        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        req = self.session.get

        if method == HttpMethod.post:
            req = self.session.post
        elif method == HttpMethod.put:
            req = self.session.put
        elif method == HttpMethod.options:
            req = self.session.options

        async with req(url, **kwargs) as resp:
            return await resp.text()

    async def _get(self, api_path: str, **kwargs: Any) -> str:
        url = urljoin(self.base_url, api_path)
        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        async with self.session.get(url, **kwargs) as resp:
            return await resp.text()

    async def _post(self, api_path: str, **kwargs: Any) -> str:
        url = urljoin(self.base_url, api_path)
        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        async with self.session.get(url, **kwargs) as resp:
            return await resp.text()

    async def _json(self, method: HttpMethod) -> None:
        pass

    async def _get_json(self, api_path: str, **kwargs: Any) -> dict[str, Any]:
        resp_txt = await self._request(api_path, HttpMethod.get, **kwargs)
        return ujson.loads(resp_txt)

    async def _post_json(self, api_path: str, **kwargs: Any) -> dict[str, Any]:
        resp_txt = await self._request(api_path, HttpMethod.post, **kwargs)
        return ujson.loads(resp_txt)

    async def close(self) -> None:
        if self.session:
            await self.session.close()
