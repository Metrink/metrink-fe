from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import select, join
from datetime import datetime
from cache import get_cache
import logging
import re
import yaml

from logger import logger
from readers.Reader import Reader


class Zabbix(Reader):
    def __init__(self):
        super().__init__()

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
        self.engine = create_engine(db_url, echo=True)
        metadata = MetaData(bind=self.engine)

        # load up the tables we care about
        # need to make this more configurable
        self.hosts_table = Table('hosts', metadata, autoload=True)
        self.items_table = Table('items', metadata, autoload=True)
        self.groups_table = Table('groups', metadata, autoload=True)
        self.hosts_groups_table = Table('hosts_groups', metadata, autoload=True)

        self.history_table = Table('history', metadata, autoload=True)
        self.history_uint_table = Table('history_uint', metadata, autoload=True)

        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def get_hosts_in_group(self, group:str):
        """
        Returns a list of dictionaries for the hosts in a group using pattern matching
        :param group: a "regular expression" of a group name
        :return: list of dicts for the hosts that are in the group
        """
        hosts = self.get_hosts()

        # build the pattern to search against
        pattern = re.compile(group.replace('*', '.*'))

        return filter(lambda h: re.match(pattern, h['group']), hosts)

    def get_hosts(self, attr=None):
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
        j1 = join(self.hosts_table, self.hosts_groups_table, self.hosts_table.c.hostid == self.hosts_groups_table.c.hostid)
        j2 = join(j1, self.groups_table, self.hosts_groups_table.c.groupid == self.groups_table.c.groupid)

        # run the select to fetch in what we want
        res = self.engine.execute(select([self.hosts_table.c.hostid, self.hosts_table.c.host, self.groups_table.c.name, self.hosts_groups_table.c.groupid]).select_from(j2))

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

    def get_items(self, attr=None):
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
        j1 = join(self.hosts_table, self.items_table, self.hosts_table.c.hostid == self.items_table.c.hostid)

        # run the select to fetch in what we want
        cols = [self.items_table.c.itemid, self.items_table.c.name, self.hosts_table.c.host, self.items_table.c.hostid, self.items_table.c.key_, self.items_table.c.value_type]
        res = self.engine.execute(select(cols).select_from(j1))

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

    def filter_metrics(self, host:str=None, group:str=None, metric:str=None):
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
        hosts = self.get_hosts()

        # compile patterns for them all
        host_patern = re.compile(host.replace('*', '.*')) if host is not None else re.compile('.*')
        group_patern = re.compile(group.replace('*', '.*')) if group is not None else re.compile('.*')
        item_patern = re.compile(metric.replace('*', '.*')) if metric is not None else re.compile('.*')

        # filter out those that don't match the host and group
        hosts = filter(lambda h: re.match(host_patern, h['host']) and re.match(group_patern, h['group']), hosts)
        host_lookup = {h['hostid']: h for h in hosts}

        # pick out the items that match the host_ids and name
        items = filter(lambda i: i['hostid'] in host_lookup.keys() and re.match(item_patern, i['name']), self.get_items())

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

    @staticmethod
    def resample_metrics(df, start, end):
        if df.empty:
            return df

        df = df.fillna(method='ffill')

        graph_range = end - start

        if graph_range.days >= 10:  # if more than 10 days of values
            logger.debug('Resampling down to 24 hours')
            df = df.resample('24H', closed='left', label='left').median()  # resample to every day
        elif graph_range.days >= 1:  # if more than 1 day of values
            logger.debug('Resampling down to 60 minutes')
            df = df.resample('60T', closed='left', label='left').median()  # resample to every 60 minutes
        elif graph_range.seconds > 43200:  # if more than 12 hours
            logger.debug('Resampling down to 10 minutes')
            df = df.resample('10T', closed='left', label='left').median()  # resample to every 10 minutes
        elif graph_range.seconds > 5400:  # if more than 1.5 hours
            logger.debug('Resampling down to 5 minutes')
            df = df.resample('5T', closed='left', label='left').median()  # resample to every 5 minutes

        # round down to the nearest second
        df.index = df.index.map(lambda i: datetime.fromtimestamp(int(i.timestamp()//10)*10))

        return df


    # for h in get_hosts_in_group('Tier-[2|3] Templates'):
    #     print(h['group'])

    # for i in get_items():
    #     print(i['name'])

