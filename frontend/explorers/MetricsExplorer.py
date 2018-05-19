
from explorers.Explorer import Explorer


class RedisCassandra(Explorer):
    def __index__(self):
        super().__init__('RedisCassandra')

    def get_template(self):
        return 'explorers/redis_cassandra.html'

