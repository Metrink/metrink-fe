import redis

from datetime import datetime
from cassandra.cluster import Cluster

from logger import logger
from readers.Reader import Reader
from configuration import Configuration


class RedisCassandraReader(Reader):
    def __init__(self, config: Configuration):
        super().__init__()

        redis_host = config.get('redis.host')
        redis_port = config.get('redis.port')

        self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port)
        logger.info("Redis configured with %s:%d" % (redis_host, redis_port))

        cass_hosts = config.get('cassandra.hosts')
        keyspace = config.get('cassandra.keyspace')

        self.cass_conn = Cluster(cass_hosts).connect(keyspace)
        logger.info("Cassandra configured with hosts %s and keyspace %s" % (','.join(cass_hosts), keyspace))

    def get_results(self, start_time: datetime, end_time: datetime, tags: dict, tags_include: dict=None):
        # get the set of Cassandra rows from Redis
        tag_search = ['%s=%s'%(k,v) for k,v in tags.items()]
        cass_tags = self.redis_conn.sinter(*tag_search)

        