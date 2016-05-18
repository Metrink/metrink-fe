import memcache

from logger import logger


class MyCache:
    mc = None

    def __init__(self, mc):
        self.mc = mc

    def get(self, key):
        ret = self.mc.get(key)

        if ret is None:
            logger.warn('Cache miss for: ' + str(key))
            #stats = self.mc.get_stats()[0][1]

            #logger.info('Hits: ' + str(stats['get_hits']) + ' Misses: ' + str(stats['get_misses']))
        return ret

    def multi_get(self, keys):
        if not hasattr(keys, '__iter__'):
            raise ValueError('Keys must be a list')

        return self.mc.get_multi(keys)

    def set(self, key, value, timeout=0):
        return self.mc.set(key, value, timeout)

    def multi_set(self, key_values, timeout=0):
        if not isinstance(key_values, dict):
            raise ValueError('Key_values must be a dictionary')

        return self.mc.set_multi(key_values, timeout)

    def delete(self, key):
        self.mc.delete(key)

    def multi_delete(self, keys):
        if not hasattr(keys, '__iter__'):
            raise ValueError('Keys must be a list')

        self.mc.delete_multi(keys)

client = MyCache(memcache.Client(['127.0.0.1:11211'], debug=0))


def get_cache():
    return client


