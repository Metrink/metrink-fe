import redis

class RedisCassandraReader(Reader):
    def __init__(self, redis_host='localhost':str, redis_port=6379:int, cass_hosts=['localhost']:array):
        self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port)
        self.cass_conn = Cluster(cass_hosts).connect()

    def get_results(self, start_time:datetime, end_time:datetime, tags:dict, tags_include=None:dict):
        # get the set of Cassandra rows from Redis
        tag_search = ['%s=%s'%(k,v) for k,v in tags.items()]
        cass_tags = self.redis_conn.sinter(*tag_search)

        