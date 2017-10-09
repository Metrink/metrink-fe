from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class AverageFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):

        if self._args is not None and len(self._args) > 2:
            raise ValueError('Invalid argument to average function')

        # get a copy of the input
        data = (input if len(self._args) == 0 else self._args[0].process(start_time, end_time, input)).copy(deep=True)

        # go through each column, get the average, and apply it to the rows
        for col in data.columns:
            avg = data[col].mean()
            data[col] = data[col].apply(lambda a: avg)
            data.rename(columns={col: 'avg ' + col}, inplace=True)

        print(data.head())

        return data
