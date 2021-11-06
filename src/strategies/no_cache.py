class CacheMock:
    @staticmethod
    async def set(*args, **kwargs):
        pass

    @staticmethod
    async def get(*args, **kwargs):
        pass

    @classmethod
    def setup(cls):
        return cls

    @staticmethod
    def close():
        pass


def init_cache_client(app, config):
    app.cache = CacheMock.setup()


def close_cache_client(app, config):
    app.cache.close()
