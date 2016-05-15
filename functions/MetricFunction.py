from datetime import datetime, timedelta
from pandas import DataFrame
from functions.QueryFunction import QueryFunction

from random import randint


class MetricFunction(QueryFunction):
    def __init__(self, host:str, group:str, name:str):
        super().__init__('metric', (host, group, name))
        self.host = str(host)
        self.group = str(group)
        self.name = str(name)

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        cur_time = start_time
        index = []
        data = []

        name = "%s:%s:%s" % (self.host, self.group, self.name)

        while cur_time < end_time:
            data.append({name: randint(0, 10)})
            index.append(cur_time)

            cur_time += timedelta(minutes=10)

        return DataFrame(data, index=index)