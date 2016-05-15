from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class AverageFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):

        if self._args is not None and len(self._args) > 2:
            raise ValueError('Invalid argument to average function')

        if len(self._args) == 0:
            # just return the column-wise mean
            return input.mean(1)
        else:
            # process the input
            return self._args[0].process(start_time, end_time, input).mean(1)
