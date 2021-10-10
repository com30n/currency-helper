from typing import Dict

import aiohttp


async def async_request(url) -> Dict:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return await response.json()
