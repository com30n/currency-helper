from enum import Enum
from urllib.parse import urljoin

import aiohttp
import ujson


class HttpMethod(Enum):
    get = "get"
    post = "post"
    put = "put"
    options = "options"


class BaseClient:
    def __init__(self, config: dict, client_name: str, *args, **kwargs):
        self.config = config
        self.client_config = config["clients"][client_name]
        self.base_url = self.client_config["base_url"]
        self._timeout = self.client_config.get("timeout", kwargs.get("timeout", 10))
        self.session = aiohttp.ClientSession(
            json_serialize=ujson.dumps,
            timeout=aiohttp.client.ClientTimeout(total=self._timeout),
        )
        self.currencies_list_cache_key = client_name
        self.session = None

    async def _request(self, api_path: str, method: HttpMethod, **kwargs) -> str:
        url = urljoin(self.base_url, api_path)

        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        if method == HttpMethod.get:
            async with self.session.get(url, **kwargs) as resp:
                return await resp.text()
        elif method == HttpMethod.post:
            async with self.session.post(url, **kwargs) as resp:
                return await resp.text()
        elif method == HttpMethod.put:
            async with self.session.put(url, **kwargs) as resp:
                return await resp.text()
        elif method == HttpMethod.options:
            async with self.session.options(url, **kwargs) as resp:
                return await resp.text()

    async def _get(self, api_path: str, **kwargs) -> str:
        url = urljoin(self.base_url, api_path)
        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        async with self.session.get(url, **kwargs) as resp:
            return await resp.text()

    async def _post(self, api_path: str, **kwargs) -> str:
        url = urljoin(self.base_url, api_path)
        if self.session is None:
            self.session = aiohttp.ClientSession(
                json_serialize=ujson.dumps,
                timeout=aiohttp.client.ClientTimeout(total=self._timeout),
            )

        async with self.session.get(url, **kwargs) as resp:
            return await resp.text()

    async def _json(self, method: HttpMethod):
        pass

    async def _get_json(self, api_path: str, **kwargs) -> dict:
        resp_txt = await self._request(api_path, HttpMethod.get, **kwargs)
        return ujson.loads(resp_txt)

    async def _post_json(self, api_path: str, **kwargs) -> dict:
        resp_txt = await self._request(api_path, HttpMethod.post, **kwargs)
        return ujson.loads(resp_txt)

    async def close(self):
        if self.session:
            await self.session.close()
