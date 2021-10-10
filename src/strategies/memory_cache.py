from cashews import cache


def init_cache_client(app, config):
    app.cache = cache.setup(config['memory']['uri'])


def close_cache_client(app):
    app.cache.close()