from datetime import datetime
from pandas import DataFrame

from frontend.functions.QueryFunction import QueryFunction
from frontend.logger import logger


class EventFunction(QueryFunction):
    def __init__(self, fields):
        super().__init__('log', fields)
        self.fields = fields

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        logger.debug('Start: %s  End: %s  Event: fields=%s' % (start_time.isoformat(), end_time.isoformat(), str(self.fields)))

        return input
