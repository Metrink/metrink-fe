from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class AbsoluteValueFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        if self._args is not None and len(self._args) > 2:
            raise ValueError('Invalid argument to absolute value function')

        if len(self._args) == 0:
            # just return the abs
            return input.abs()
        else:
            # process the input
            return self._args[0].process(start_time, end_time, input).abs() if isinstance(self._args[0], QueryFunction) else abs(self._args[0])
