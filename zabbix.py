from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import select, join
from cache import get_cache
import logging
import re

from functions.QueryFunction import QueryFunction
from logger import logger

# this seems like a terrible and inefficient way to go about things
# setup the engine per http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#sql-abstraction-layer
engine = create_engine('mysql+mysqldb://metrink:metrink@10.0.128.44/zabbix', echo=True)
metadata = MetaData(bind=engine)

# load up the tables we care about
# need to make this more configurable
hosts_table = Table('hosts', metadata, autoload=True)
history_table = Table('history', metadata, autoload=True)
items_table = Table('items', metadata, autoload=True)
groups_table = Table('groups', metadata, autoload=True)
hosts_groups_table = Table('hosts_groups', metadata, autoload=True)

print('IN HERE')

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_hosts_in_group(group:str):
    """
    Returns a list of dictionaries for the hosts in a group using pattern matching
    :param group: a "regular expression" of a group name
    :return: list of dicts for the hosts that are in the group
    """
    hosts = get_hosts()

    # build the pattern to search against
    pattern = re.compile(group.replace('*', '.*'))

    return filter(lambda h: re.match(pattern, h['group']), hosts)


def get_hosts(attr=None):
    """
    Gets a list of dictionaries of hosts with associated groups
    :param attr return a unique list of only that attribute, None = full dictionary
    :return:
    """
    cache = get_cache()

    hosts = cache.get('hosts')

    if hosts is not None:
        # pull out an attribute if we're looking for one
        # removes duplicates as well
        if attr is not None:
            hosts = list(set([h[attr] for h in hosts]))

        return hosts

    # join in the tables
    j1 = join(hosts_table, hosts_groups_table, hosts_table.c.hostid == hosts_groups_table.c.hostid)
    j2 = join(j1, groups_table, hosts_groups_table.c.groupid == groups_table.c.groupid)

    # run the select to fetch in what we want
    res = engine.execute(select([hosts_table.c.hostid, hosts_table.c.host, groups_table.c.name, hosts_groups_table.c.groupid]).select_from(j2))

    hosts = []

    for row in res:
        hosts.append({
            'hostid': row[0],
            'host': row[1],
            'group': row[2],
            'groupid': row[3]
        })

    cache.set('hosts', hosts)

    # pull out an attribute if we're looking for one
    # removes duplicates as well
    if attr is not None:
        hosts = list(set([h[attr] for h in hosts]))

    return hosts

# for h in get_hosts_in_group('Tier-[2|3] Templates'):
#     print(h['group'])