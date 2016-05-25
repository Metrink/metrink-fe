from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import select, join
from cache import get_cache
import logging
import re
import yaml

from logger import logger

config = None
with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except ImportError as e:
        print('Error opening config file: ' + str(e))
        exit(1)

# this seems like a terrible and inefficient way to go about things
# setup the engine per http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#sql-abstraction-layer
db_url = 'mysql+mysqldb://%s:%s@%s/zabbix' % (config['db_user'], config['db_pass'], config['db_host'])
engine = create_engine(db_url, echo=True)
metadata = MetaData(bind=engine)

# load up the tables we care about
# need to make this more configurable
hosts_table = Table('hosts', metadata, autoload=True)
items_table = Table('items', metadata, autoload=True)
groups_table = Table('groups', metadata, autoload=True)
hosts_groups_table = Table('hosts_groups', metadata, autoload=True)

history_table = Table('history', metadata, autoload=True)
history_uint_table = Table('history_uint', metadata, autoload=True)

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

    cache.set('hosts', hosts, timeout=43200)  # cache for 12 hours

    # pull out an attribute if we're looking for one
    # removes duplicates as well
    if attr is not None:
        hosts = list(set([h[attr] for h in hosts]))

    return hosts


def get_items(attr=None):
    """
    Gets a list of dictionaries of items
    :param attr:  return a unique list of only that attribute, None = full dictionary
    :return:
    """
    cache = get_cache()

    items = cache.get('items')

    if items is not None:
        # pull out an attribute if we're looking for one
        # removes duplicates as well
        if attr is not None:
            items = list(set([h[attr] for h in items]))

        return items

    # join in the tables
    j1 = join(hosts_table, items_table, hosts_table.c.hostid == items_table.c.hostid)

    # run the select to fetch in what we want
    cols = [items_table.c.itemid, items_table.c.name, hosts_table.c.host, items_table.c.hostid, items_table.c.key_, items_table.c.value_type]
    res = engine.execute(select(cols).select_from(j1))

    items = []

    for row in res:
        name = row[1]

        if '$' in name:
            keys = row[4][row[4].index('[')+1:row[4].index(']')].split(',')

            for k in re.findall('\$\d+', name):
                name = name.replace(k, keys[int(k[1:])-1])

        items.append({
            'itemid': row[0],
            'name': name,
            'host': row[2],
            'hostid': row[3],
            'value_type': row[5]
        })

    cache.set('items', items, timeout=43200)

    # pull out an attribute if we're looking for one
    # removes duplicates as well
    if attr is not None:
        items = list(set([h[attr] for h in items]))

    return items


def filter_metrics(host:str=None, group:str=None, metric:str=None):
    """
    Filters out all of the metrics based on host, group, and metric name
    :param host:
    :param group:
    :param metric:
    :return:
    """

    if host is None and group is None and metric is None:
        logger.warn('Tried to ask for full table of data')
        return []  # we shouldn't go returning everything

    # get hosts and groups
    hosts = get_hosts()

    # compile patterns for them all
    host_patern = re.compile(host.replace('*', '.*')) if host is not None else re.compile('.*')
    group_patern = re.compile(group.replace('*', '.*')) if group is not None else re.compile('.*')
    item_patern = re.compile(metric.replace('*', '.*')) if metric is not None else re.compile('.*')

    # filter out those that don't match the host and group
    hosts = filter(lambda h: re.match(host_patern, h['host']) and re.match(group_patern, h['group']), hosts)
    host_lookup = {h['hostid']: h for h in hosts}

    # pick out the items that match the host_ids and name
    items = filter(lambda i: i['hostid'] in host_lookup.keys() and re.match(item_patern, i['name']), get_items())

    ret = []

    for i in items:
        if i['hostid'] in host_lookup.keys():
            h = host_lookup[i['hostid']]
            ret.append({
                'host': h['host'],
                'hostid': h['hostid'],
                'group': h['group'],
                'groupid': h['groupid'],
                'item': i['name'],
                'itemid': i['itemid'],
                'value_type': i['value_type']
            })

    return ret

# for h in get_hosts_in_group('Tier-[2|3] Templates'):
#     print(h['group'])

# for i in get_items():
#     print(i['name'])
