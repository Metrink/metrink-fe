from datetime import datetime, timedelta
from pandas import DataFrame, read_sql
from random import randint
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import select
import logging

from functions.QueryFunction import QueryFunction
from logger import logger
import os, sys

# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zabbix import engine, hosts_table, items_table, history_table


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

        # get the host id
        res = hosts_table.select(hosts_table.c.host == self.host).execute().first()

        if res is None:
            logger.warn('Unknown host: ' + str(self.host))
            return input

        host_id = res[0]

        res = items_table.select(and_(items_table.c.name == self.name, items_table.c.hostid == host_id)).execute().first()

        if res is None:
            logger.warn('Unknown item/metric: ' + str(self.name))
            return input

        item_id = res[0]

        print('HOSTID: %d ITEMID: %d' % (host_id, item_id))

        ret = read_sql(select([history_table.c.clock, history_table.c.value]).where(history_table.c.itemid == item_id), engine, parse_dates=('clock', ), index_col='clock')

        # rename to the metric
        metric_name = "%s:%s:%s" % (self.host, self.group, self.name)
        ret.columns = [metric_name]

        print(ret.head())
        print(ret.tail())


        return ret

        # metric_name = "%s:%s:%s" % (self.host, self.group, self.name)
        #
        # while cur_time < end_time:
        #     data.append({metric_name: randint(0, 10)})
        #     index.append(cur_time)
        #
        #     cur_time += timedelta(minutes=10)
        #
        # return DataFrame(data, index=index)


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