from datetime import datetime

from pandas import DataFrame, read_sql
from sqlalchemy import and_
from sqlalchemy.sql import select

from frontend.functions.QueryFunction import QueryFunction
from frontend.logger import logger


class MetricFunction(QueryFunction):
    def __init__(self, fields, overlay=None):
        super().__init__('metric', (fields, overlay))
        self.fields = fields
        self.overlay = overlay

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        cur_time = start_time
        index = []
        data = []

        # expand the hosts and groups
        metric_list = self.reader.filter_metrics(self.fields.get('host', None), self.fields.get('group', None), self.fields.get('metric', None))

        logger.debug('Got a list of %d metrics to pull from db' % (len(metric_list), ))

        ret = DataFrame()

        return ret


