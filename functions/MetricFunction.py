from datetime import datetime, timedelta
from flask import g
from pandas import DataFrame
from random import randint
from sqlalchemy.sql import select

from functions.QueryFunction import QueryFunction


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

        res = g.db.execute('select * from hosts')


        name = "%s:%s:%s" % (self.host, self.group, self.name)

        while cur_time < end_time:
            data.append({name: randint(0, 10)})
            index.append(cur_time)

            cur_time += timedelta(minutes=10)

        return DataFrame(data, index=index)


#
# Zabbix Tables
#
#   history - stores the actual metric information
#       itemid - links to the item the metric is for
#       clock - the timestamp: from_unixtime(clock)
#       value - the value of the metric
#
#   items - used to store "metric" names
#       itemid - primary key
#       name - name of the metric
#       hostid - the id of the host it relates to
#       description - a description of the item
#
#   hosts - stores the hosts on the system
#       hostid - the unique ID of the hosts
#       host - the name of the host
#
#   groups - the groups associated with hosts
#       groupid - primary key
#       name - the name of the group
#
#   hosts_groups - the mapping of hosts into groups
#       hostgroupid - primary key
#       hostid - the ID of the host
#       groupid - the ID of the group
#
# select hostid from hosts where host = 'host'
# select itemid from items where hostid = hostid
# select clock, value from history where itemid = itemid
#