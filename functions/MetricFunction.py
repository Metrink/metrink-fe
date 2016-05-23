from datetime import datetime, timedelta
from pandas import DataFrame, read_sql
from sqlalchemy import and_
from sqlalchemy.sql import select
import logging

from functions.QueryFunction import QueryFunction
from logger import logger
from zabbix import filter_metrics
import os, sys

# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zabbix import engine, hosts_table, items_table, history_table


class MetricFunction(QueryFunction):
    def __init__(self, host:str, group:str, metric:str):
        super().__init__('metric', (host, group, metric))
        self.host = str(host)
        self.group = str(group)
        self.metric = str(metric)

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        cur_time = start_time
        index = []
        data = []

        # expand the hosts and groups
        metric_list = filter_metrics(self.host, self.group, self.metric)

        logger.debug('Got a list of %d metrics to pull from db' % (len(metric_list), ))

        ret = DataFrame()

        # go through and read the data one item at a time
        for metric in metric_list:
            cond = and_(history_table.c.itemid == metric['itemid'], history_table.c.clock > start_time.timestamp())
            cond = and_(cond, history_table.c.clock < end_time.timestamp())
            data = read_sql(select([history_table.c.clock, history_table.c.value]).where(cond), engine, parse_dates=('clock', ), index_col='clock')

            # rename to the metric
            metric_name = "%s:%s:%s" % (metric['host'], metric['group'], metric['item'])
            data.columns = [metric_name]

            ret = ret.combine_first(data)

        print(ret.head())

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
#       type:
#         0 - Zabbix agent;
#         1 - SNMPv1 agent;
#         2 - Zabbix trapper;
#         3 - simple check;
#         4 - SNMPv2 agent;
#         5 - Zabbix internal;
#         6 - SNMPv3 agent;
#         7 - Zabbix agent(active);
#         8 - Zabbix aggregate;
#         9 - web item;
#         10 - external check;
#         11 - database monitor;
#         12 - IPMI agent;
#         13 - SSH agent;
#         14 - TELNET agent;
#         15 - calculated;
#         16 - JMX agent.
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