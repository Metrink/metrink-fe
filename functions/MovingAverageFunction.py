from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class MovingAverageFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        pass
