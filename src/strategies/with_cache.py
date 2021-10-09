import fastapi
from aioredis.client import Redis


def setup_cache_client(app: fastapi, config: dict):
    async def init_cache_client(app):
        app['cache'] = CacheClient.from_url(config['REDIS_URI'])

    async def close_cache_client(app):
        await app['cache'].close()

    app.on_startup.append(init_cache_client)
    app.on_shutdown.append(close_cache_client)


class CacheClient(Redis):
    def __init__(self):
        super().__init__()
