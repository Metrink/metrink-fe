from redis import StrictRedis
from configuration import Configuration
from explorers.Explorer import Explorer
from cache import get_cache


class MetricsExplorer(Explorer):
    def __init__(self, config: Configuration):
        super().__init__('RedisCassandra')
        redis_host = config.get('redis.host')
        redis_port = config.get('redis.port')
        redis_pass = config.get('redis.password')

        #TODO: change to Sentinel so we can handle multiple hosts
        self.redis_conn = StrictRedis(host=redis_host, port=redis_port, password=redis_pass)
        self.cache = get_cache()

    def get_template(self):
        return 'explorers/metrics.html'

    def get_table_data(self):
        ret = self.cache.get('_tname')

        if ret is not None:
            return ret

        tag_names = self.redis_conn.smembers('_tname')
        tag_names = [t.decode() for t in tag_names]

        pipeline = self.redis_conn.pipeline()  # setup a pipeline

        for tag_name in tag_names:
            # {'tag': name.decode()}
            pipeline.smembers('_t|%s'%tag_name)

        values = pipeline.execute()

        ret = []

        for i in range(len(tag_names)):
            ret.append({'tag': tag_names[i], 'values': [v.decode() for v in values[i]]})

        self.cache.set('_tname', ret)

        return ret

