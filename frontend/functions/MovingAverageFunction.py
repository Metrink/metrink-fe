from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class MovingAverageFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):

        if self._args is None or len(self._args) > 1:
            raise ValueError('Invalid number of arguments to mavg')

        return input.resample(self._args[0]).fillna('nearest').rolling(window=3).mean()
