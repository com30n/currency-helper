from functools import partial

from . import memory_cache, no_cache, redis_cache


def setup_cache_client(app, config: dict):
    cache_config = config.get('cache', {})
    if cache_config.get('redis', {}).get('enabled', None):
        redis_cache.init_cache_client(app=app, config=config)

    elif cache_config.get('memory').get('enabled', None):
        memory_cache.init_cache_client(app=app, config=config)
    else:
        no_cache.init_cache_client(app=app, config=config)
