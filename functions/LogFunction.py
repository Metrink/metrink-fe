from datetime import datetime
from pandas import DataFrame

from functions.QueryFunction import QueryFunction
from logger import logger


class LogFunction(QueryFunction):
    def __init__(self, indices, fields):
        super().__init__('log', (indices, fields))
        self.indices = indices
        self.fields = fields

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        logger.debug('Got log for %s and fields %s' % (str(self.indices), str(self.fields)))