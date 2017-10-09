from datetime import datetime
from pandas import DataFrame

from frontend.functions.QueryFunction import QueryFunction


class GraphFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):

        return input
